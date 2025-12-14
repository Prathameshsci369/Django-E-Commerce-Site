from django.core.management.base import BaseCommand
from products.models import Product, ProductImage
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Downloads and adds images to all products'

    def handle(self, *args, **options):
        # Get all products to ensure we can find images for them
        products = Product.objects.all()
        
        # A dictionary mapping product slugs to their respective image URLs
        # These are new URLs for all 25 products.
        image_urls = {
            'wireless-headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop',
            'smart-watch': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&h=600&fit=crop',
            'cotton-t-shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=600&fit=crop',
            'programming-book': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&h=600&fit=crop',
            'laptop-stand': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=600&fit=crop',
            '4k-webcam': 'https://images.unsplash.com/photo-1592659762303-90081d34b277?w=800&h=600&fit=crop',
            'bluetooth-speaker': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=600&fit=crop',
            'usb-c-hub': 'https://images.unsplash.com/photo-1628695456048-3a5f2c9b6c8a?w=800&h=600&fit=crop',
            'mechanical-keyboard': 'https://images.unsplash.com/photo-1596178065887-11982b95699b?w=800&h=600&fit=crop',
            'wireless-mouse': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&h=600&fit=crop',
            'denim-jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=600&fit=crop',
            'winter-jacket': 'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=800&h=600&fit=crop',
            'running-shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=600&fit=crop',
            'wool-sweater': 'https://images.unsplash.com/photo-1576871335025-fd32a706f691?w=800&h=600&fit=crop',
            'leather-belt': 'https://images.unsplash.com/photo-1520870668631-c359b5882673?w=800&h=600&fit=crop',
            'scifi-novel': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=600&fit=crop',
            'cookbook': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
            'history-encyclopedia': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',
            'coffee-maker': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=600&fit=crop',
            'air-fryer': 'https://images.unsplash.com/photo-1562565402-f3e8d8331a84?w=800&h=600&fit=crop',
            'non-stick-pan': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop',
            'water-bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800&h=600&fit=crop',
            'yoga-mat': 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=800&h=600&fit=crop',
            'desk-lamp': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop', # Using a different image for variety
            'board-game': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=800&h=600&fit=crop',
        }

        for product in products:
            # Check if a URL exists for the product and if it doesn't already have an image
            if product.slug in image_urls and not product.images.exists():
                try:
                    response = requests.get(image_urls[product.slug], stream=True)
                    if response.status_code == 200:
                        # Name the image file based on the product slug
                        image_name = f"{product.slug}.jpg"
                        
                        # Create the ProductImage object
                        ProductImage.objects.create(
                            product=product,
                            image=ContentFile(response.content, name=image_name),
                            alt_text=product.name,
                            is_primary=True
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully added image for: {product.name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to download image for {product.name}. Status code: {response.status_code}')
                        )
                except requests.exceptions.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(f'Could not download image for {product.name}: {e}')
                    )
            elif product.images.exists():
                 self.stdout.write(
                    self.style.NOTICE(f'Image already exists for: {product.name}. Skipping.')
                )
            else:
                 self.stdout.write(
                    self.style.WARNING(f'No image URL found for product slug: {product.slug}. Skipping.')
                )

        self.stdout.write(self.style.SUCCESS('Image processing complete.'))
