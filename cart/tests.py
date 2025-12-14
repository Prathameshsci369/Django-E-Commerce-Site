#from django.test import TestCase

# Create your tests here.
# from Bio import Entrez
# import time # NCBI ला एकाच वेळी खूप जास्त रिक्वेस्ट पाठवू नये म्हणून delay साठी
# from io import StringIO # स्ट्रिंगला फाईलप्रमाणे हाताळण्यासाठी

# # 1. ओळख सेट करणे (Set Identification)
# # *तुम्ही तुमचा खरा ईमेल ID येथे वापरायला हवा*
# Entrez.email = "jomehi@fxzig.com" 

# # 2. efetch वापरून डेटा डाऊनलोड करणे (Downloading data using efetch)
# # ID: NM_001005 ही प्रथिन सिक्वेन्सची ID नाही. ती एका mRNA (nucleotide) ची ID आहे.
# # आपण 'P0C0L5' या AlphaFold द्वारे विश्लेषण केलेल्या प्रोटीनचा ID वापरूया, जो तुमच्या मागणीशी जुळेल.

# try:
#     print("--- NCBI डेटाबेसवरून FASTA क्रम डाऊनलोड करत आहे... ---")
    
#     # Entrez.efetch ला रिक्वेस्ट पाठवणे
#     handle = Entrez.efetch(
#         db="protein",  # प्रथिन डेटाबेस
#         id="P0C0L5",    # AlphaFold मध्ये वापरला जाणारा एक प्रथिन ID (उदा. Human Ubiquitin)
#         rettype="fasta", # FASTA फॉरमॅटमध्ये डेटा हवा
#         retmode="text"   # साध्या टेक्स्टमध्ये डेटा हवा
#     )
    
#     # हँडलमधून डेटा वाचणे (Reading data from the handle)
#     fasta_data = handle.read()
#     handle.close()
    
#     print("\n[ डाऊनलोड झालेला FASTA डेटा ]")
#     print(fasta_data)
    
#     # तुम्ही डाऊनलोड केलेला डेटा फाईलमध्ये सेव्ह करू शकता:
#     with open("P0C0L5_protein.fasta", "w") as out_handle:
#         out_handle.write(fasta_data)
        
# except Exception as e:
#     print(f"\nत्रुटी (Error) आली: {e}")
#     print("कृपया तुमचा ईमेल ID बरोबर असल्याची आणि इंटरनेट जोडणी असल्याची खात्री करा.")

# # 3. शिष्टाचार: पुढची रिक्वेस्ट करण्यापूर्वी थोडा वेळ थांबा
# time.sleep(1) 
# print("--- डाऊनलोड पूर्ण ---")


# from Bio import SeqIO 
# from Bio.Seq import Seq
# #create seq objects 
# dna_sequence = Seq("AGTGCAGTG")
# #trancription DNA T to RNA A
# rna_sequence = dna_sequence.transcribe() 
# #translation RNA to Protein

# protein_sequence = rna_sequence.translate()

# print(f"DNA Sequence: {dna_sequence}")
# print(f"RNA Sequence: {rna_sequence}")
# print(f"Protein Sequence: {protein_sequence}")  

# #4. using seqio to read fasta file 

# try:
#     print("### Reading FASTA file using SeqIO ###" \
#     "n-----------------------------------")
#     for  record in SeqIO.parse("P0C0L5_protein.fasta", "fasta"):
#         print(f"ID: {record.id}")
#         print(f"Description: {record.description}")
#         print(f"Sequence: {record.seq}")
#         print(f"Length: {len(record.seq)} amino acids")
# except FileNotFoundError:
#     print("FASTA file not found. Please ensure the file 'P0C0L5_protein.fasta' exists in the current directory.")


from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO 
from Bio.Seq import Seq
from io import StringIO
from Bio.SeqRecord import SeqRecord
import logging
import sys
import time
from datetime import datetime, timezone

# Configure logging: writes to stdout and appends to cart_blast.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("cart_blast.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)
dna_sequence = Seq("ATCCGGTCCGGTATTAGGGCGTACG")

record = SeqRecord(dna_sequence, id="query1", description="")
buf = StringIO()
SeqIO.write(record, buf, "fasta")
fasta_string = buf.getvalue()

# remote BLAST request
logger.info("### Performing BLAST search ###")
logger.debug("FASTA query:\n%s", fasta_string)

result_handle = None
try:
    start_time = time.time()
    result_handle = NCBIWWW.qblast(
        program="blastn",
        database="nr",
        sequence=fasta_string,
        hitlist_size=10,  # ask for up to 10 hits
    )

    # Read the raw XML response so we can both parse it and optionally save it for debugging.
    xml_text = result_handle.read()
    elapsed = time.time() - start_time
    logger.info("BLAST request completed in %.2f seconds", elapsed)

    # Close the HTTP handle now that we've consumed it.
    try:
        result_handle.close()
    except Exception:
        logger.debug("Failed to close result_handle after read", exc_info=True)

    blast_records = NCBIXML.parse(StringIO(xml_text))

    any_record = False
    for blast_record in blast_records:
        any_record = True
        total_hits = len(blast_record.alignments)
        if total_hits == 0:
            logger.info("[ Blast Results ] No hits found for the query.")
            # save raw XML for debugging
            fname = f"cart_blast_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.xml"
            try:
                with open(fname, "w") as fh:
                    fh.write(xml_text)
                logger.info("Saved raw BLAST XML to %s for debugging", fname)
            except Exception:
                logger.debug("Failed to save raw BLAST XML", exc_info=True)
            break

        logger.info("[ Blast Results - first %d hits ]", min(5, total_hits))
        for alignment in blast_record.alignments[:5]:
            logger.info("%s", "-" * 60)
            # alignment.title can be long; log full title at DEBUG and short at INFO
            logger.info("Title: %s", (alignment.title[:120] + "...") if len(alignment.title) > 120 else alignment.title)
            hsp = alignment.hsps[0]
            logger.info("E-value: %s", hsp.expect)
            logger.info("Score: %s", hsp.score)
            # Log short alignment summary at INFO, full sequences at DEBUG
            logger.info("Alignment (query/match/sbjct snippet):")
            logger.info("%s", (hsp.query[:75] + "...") if len(hsp.query) > 75 else hsp.query)
            logger.info("%s", (hsp.match[:75] + "...") if len(hsp.match) > 75 else hsp.match)
            logger.info("%s", (hsp.sbjct[:75] + "...") if len(hsp.sbjct) > 75 else hsp.sbjct)
            logger.debug("Full HSP query: %s", getattr(hsp, 'query', ''))
            logger.debug("Full HSP match: %s", getattr(hsp, 'match', ''))
            logger.debug("Full HSP sbjct: %s", getattr(hsp, 'sbjct', ''))

        break

    if not any_record:
        logger.info("No BLAST records returned by NCBIXML.parse().")

except Exception as e:
    logger.exception("BLAST request/parse failed: %s", e)

finally:
    # result_handle may already be closed; try to close if it's still open
    if result_handle is not None:
        try:
            result_handle.close()
        except Exception:
            logger.debug("Failed to close result_handle cleanly in finally", exc_info=True)

logger.info("--- BLAST search complete ---")