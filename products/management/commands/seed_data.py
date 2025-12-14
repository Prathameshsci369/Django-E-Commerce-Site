from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage, ProductVarient  # Use ProductVarient
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        # Create categories
        electronics, _ = Category.objects.get_or_create(
            slug='electronics',
            defaults={
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets'
            }
        )

        clothing, _ = Category.objects.get_or_create(
            slug='clothing',
            defaults={
                'name': 'Clothing',
                'description': 'Fashion and apparel'
            }
        )

        books, _ = Category.objects.get_or_create(
            slug='books',
            defaults={
                'name': 'Books',
                'description': 'Books and literature'
            }
        )

        # Create a new category for more variety
        home_kitchen, _ = Category.objects.get_or_create(
            slug='home-kitchen',
            defaults={
                'name': 'Home & Kitchen',
                'description': 'Appliances, cookware, and home goods'
            }
        )

        # Sample products
        products_data = [
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': Decimal('199.99'),
                'compare_price': Decimal('299.99'),
                'sku': 'WH-001',
                'quantity': 50,
                'category': electronics,
                'is_featured': True,
            },
            {
                'name': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Feature-rich smartwatch with health tracking',
                'price': Decimal('299.99'),
                'compare_price': Decimal('399.99'),
                'sku': 'SW-002',
                'quantity': 30,
                'category': electronics,
                'is_featured': True,
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'description': 'Comfortable 100% cotton t-shirt',
                'price': Decimal('29.99'),
                'compare_price': Decimal('39.99'),
                'sku': 'CT-003',
                'quantity': 100,
                'category': clothing,
                'is_featured': False,
            },
            {
                'name': 'Programming Book',
                'slug': 'programming-book',
                'description': 'Learn programming from scratch',
                'price': Decimal('49.99'),
                'compare_price': Decimal('69.99'),
                'sku': 'PB-004',
                'quantity': 20,
                'category': books,
                'is_featured': False,
            },
            {
                'name': 'Laptop Stand',
                'slug': 'laptop-stand',
                'description': 'Adjustable aluminum laptop stand',
                'price': Decimal('79.99'),
                'compare_price': Decimal('99.99'),
                'sku': 'LS-005',
                'quantity': 40,
                'category': electronics,
                'is_featured': True,
            },
            # === START: 20 New Products ===
            {
                'name': '4K Webcam',
                'slug': '4k-webcam',
                'description': 'Crystal clear video for streaming and video calls.',
                'price': Decimal('149.99'),
                'compare_price': Decimal('199.99'),
                'sku': 'EW-006',
                'quantity': 60,
                'category': electronics,
                'is_featured': True,
            },
            {
                'name': 'Bluetooth Speaker',
                'slug': 'bluetooth-speaker',
                'description': 'Portable speaker with 360-degree sound.',
                'price': Decimal('79.99'),
                'compare_price': Decimal('99.99'),
                'sku': 'BS-007',
                'quantity': 75,
                'category': electronics,
                'is_featured': False,
            },
            {
                'name': 'USB-C Hub',
                'slug': 'usb-c-hub',
                'description': '7-in-1 adapter with HDMI, USB 3.0, and SD card reader.',
                'price': Decimal('49.99'),
                'compare_price': Decimal('59.99'),
                'sku': 'UH-008',
                'quantity': 90,
                'category': electronics,
                'is_featured': False,
            },
            {
                'name': 'Mechanical Keyboard',
                'slug': 'mechanical-keyboard',
                'description': 'RGB backlit gaming keyboard with blue switches.',
                'price': Decimal('119.99'),
                'compare_price': Decimal('159.99'),
                'sku': 'MK-009',
                'quantity': 35,
                'category': electronics,
                'is_featured': True,
            },
            {
                'name': 'Wireless Mouse',
                'slug': 'wireless-mouse',
                'description': 'Ergonomic mouse with precision tracking.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'WM-010',
                'quantity': 120,
                'category': electronics,
                'is_featured': False,
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic fit, straight-leg denim jeans.',
                'price': Decimal('89.99'),
                'compare_price': Decimal('119.99'),
                'sku': 'DJ-011',
                'quantity': 80,
                'category': clothing,
                'is_featured': True,
            },
            {
                'name': 'Winter Jacket',
                'slug': 'winter-jacket',
                'description': 'Warm and waterproof winter jacket.',
                'price': Decimal('199.99'),
                'compare_price': Decimal('249.99'),
                'sku': 'WJ-012',
                'quantity': 40,
                'category': clothing,
                'is_featured': False,
            },
            {
                'name': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Lightweight and breathable running shoes.',
                'price': Decimal('129.99'),
                'compare_price': Decimal('169.99'),
                'sku': 'RS-013',
                'quantity': 65,
                'category': clothing,
                'is_featured': True,
            },
            {
                'name': 'Wool Sweater',
                'slug': 'wool-sweater',
                'description': 'Cozy merino wool sweater.',
                'price': Decimal('99.99'),
                'compare_price': Decimal('139.99'),
                'sku': 'WS-014',
                'quantity': 50,
                'category': clothing,
                'is_featured': False,
            },
            {
                'name': 'Leather Belt',
                'slug': 'leather-belt',
                'description': 'Genuine leather belt with a classic buckle.',
                'price': Decimal('49.99'),
                'compare_price': Decimal('69.99'),
                'sku': 'LB-015',
                'quantity': 100,
                'category': clothing,
                'is_featured': False,
            },
            {
                'name': 'Science Fiction Novel',
                'slug': 'scifi-novel',
                'description': 'An epic journey through space and time.',
                'price': Decimal('24.99'),
                'compare_price': Decimal('29.99'),
                'sku': 'SN-016',
                'quantity': 150,
                'category': books,
                'is_featured': False,
            },
            {
                'name': 'Cookbook',
                'slug': 'cookbook',
                'description': 'Easy and delicious recipes for every day.',
                'price': Decimal('34.99'),
                'compare_price': Decimal('44.99'),
                'sku': 'CB-017',
                'quantity': 110,
                'category': books,
                'is_featured': True,
            },
            {
                'name': 'History Encyclopedia',
                'slug': 'history-encyclopedia',
                'description': 'A comprehensive guide to world history.',
                'price': Decimal('59.99'),
                'compare_price': Decimal('79.99'),
                'sku': 'HE-018',
                'quantity': 30,
                'category': books,
                'is_featured': False,
            },
            {
                'name': 'Coffee Maker',
                'slug': 'coffee-maker',
                'description': '12-cup programmable coffee maker.',
                'price': Decimal('79.99'),
                'compare_price': Decimal('99.99'),
                'sku': 'CM-019',
                'quantity': 55,
                'category': home_kitchen,
                'is_featured': True,
            },
            {
                'name': 'Air Fryer',
                'slug': 'air-fryer',
                'description': '5.8 quart air fryer for healthy frying.',
                'price': Decimal('99.99'),
                'compare_price': Decimal('129.99'),
                'sku': 'AF-020',
                'quantity': 70,
                'category': home_kitchen,
                'is_featured': True,
            },
            {
                'name': 'Non-Stick Frying Pan',
                'slug': 'non-stick-pan',
                'description': '10-inch ceramic non-stick frying pan.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'NP-021',
                'quantity': 95,
                'category': home_kitchen,
                'is_featured': False,
            },
            {
                'name': 'Stainless Steel Water Bottle',
                'slug': 'water-bottle',
                'description': 'Insulated water bottle that keeps drinks cold for 24 hours.',
                'price': Decimal('29.99'),
                'compare_price': Decimal('39.99'),
                'sku': 'WB-022',
                'quantity': 200,
                'category': home_kitchen,
                'is_featured': False,
            },
            {
                'name': 'Yoga Mat',
                'slug': 'yoga-mat',
                'description': 'Extra thick, non-slip exercise and yoga mat.',
                'price': Decimal('34.99'),
                'compare_price': Decimal('44.99'),
                'sku': 'YM-023',
                'quantity': 130,
                'category': home_kitchen,
                'is_featured': False,
            },
            {
                'name': 'Desk Lamp',
                'slug': 'desk-lamp',
                'description': 'LED desk lamp with adjustable brightness and color.',
                'price': Decimal('44.99'),
                'compare_price': Decimal('59.99'),
                'sku': 'DL-024',
                'quantity': 85,
                'category': home_kitchen,
                'is_featured': False,
            },
            {
                'name': 'Board Game',
                'slug': 'board-game',
                'description': 'A fun strategy game for the whole family.',
                'price': Decimal('39.99'),
                'compare_price': Decimal('49.99'),
                'sku': 'BG-025',
                'quantity': 60,
                'category': books, # Categorizing with books/games
                'is_featured': False,
            },
            # === END: 20 New Products ===
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            
            if created:
                # Add variants for some products
                if product.slug == 'wireless-headphones':
                    ProductVarient.objects.create(  # Use ProductVarient
                        product=product,
                        name='Color',
                        value='Black',
                        quantity=25
                    )
                    ProductVarient.objects.create(  # Use ProductVarient
                        product=product,
                        name='Color',
                        value='White',
                        quantity=25
                    )
                elif product.slug == 'smart-watch':
                    ProductVarient.objects.create(  # Use ProductVarient
                        product=product,
                        name='Size',
                        value='42mm',
                        quantity=15
                    )
                    ProductVarient.objects.create(  # Use ProductVarient
                        product=product,
                        name='Size',
                        value='46mm',
                        quantity=15
                    )
                elif product.slug == 'cotton-t-shirt':
                    sizes = ['S', 'M', 'L', 'XL']
                    for size in sizes:
                        ProductVarient.objects.create(  # Use ProductVarient
                            product=product,
                            name='Size',
                            value=size,
                            quantity=25
                        )
                elif product.slug == 'denim-jeans':
                    sizes = ['30', '32', '34', '36']
                    for size in sizes:
                        ProductVarient.objects.create(
                            product=product,
                            name='Waist Size',
                            value=size,
                            quantity=20
                        )
                elif product.slug == 'running-shoes':
                    ProductVarient.objects.create(
                        product=product,
                        name='Size',
                        value='9',
                        quantity=20
                    )
                    ProductVarient.objects.create(
                        product=product,
                        name='Size',
                        value='10',
                        quantity=25
                    )
                    ProductVarient.objects.create(
                        product=product,
                        name='Size',
                        value='11',
                        quantity=20
                    )

                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Database seeded successfully!')
        )