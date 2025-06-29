from django.core.management.base import BaseCommand
from inventory.models import Product, Supplier

class Command(BaseCommand):
    help = 'Seed the database with initial Boba Stop inventory data'

    def handle(self, *args, **options):
        self.stdout.write('🧋 Seeding Boba Stop inventory data...')

        # Create suppliers first
        suppliers_data = [
            {
                'name': 'Kingleke',
                'address': '3315 14th Ave Markham, ON L3R 0H3',
                'phone': '905 947 9033',
                'email': 'info@kingleke.ca',
                'website': 'www.kingleke.ca',
                'description': 'Premium tea and ingredient supplier specializing in bubble tea products'
            },
            {
                'name': 'QualiTea',
                'address': 'Unit B 96 Steelcase Road West Markham ON L3R 3J9',
                'phone': '905 622 6688',
                'email': '',
                'website': '',
                'description': 'Quality syrups, powders and bubble tea equipment supplier'
            },
            {
                'name': 'TAAS',
                'address': '1160 Bellany Road North Scarborough ON M1H 1H2',
                'phone': '416 754 4222',
                'email': 'info@tomenterprisesltd.com',
                'website': '',
                'description': 'Packaging and disposable supplies for food service industry'
            }
        ]

        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults=supplier_data
            )
            if created:
                self.stdout.write(f'✅ Created supplier: {supplier.name}')

        # Create products
        products_data = [
            # TAAS Products
            {'name': 'Dome Lid for Paper Coffee (white)', 'supplier': 'TAAS', 'quantity': 20, 'price': 2.50, 'unit': '50/sleeve'},
            {'name': 'Clear Cup 16oz', 'supplier': 'TAAS', 'quantity': 25, 'price': 45.00, 'unit': '50/pack'},
            {'name': 'Clear Cup 12oz', 'supplier': 'TAAS', 'quantity': 20, 'price': 40.00, 'unit': '50/pack'},
            {'name': 'Flat LID for 12-24oz', 'supplier': 'TAAS', 'quantity': 30, 'price': 35.00, 'unit': '100/pack'},
            {'name': 'Paper Coffee Cup 8oz', 'supplier': 'TAAS', 'quantity': 15, 'price': 25.00, 'unit': '50/pack'},

            # Kingleke Products
            {'name': 'Ceylon Black Tea', 'supplier': 'Kingleke', 'quantity': 10, 'price': 15.99, 'unit': '1kg bag'},
            {'name': 'Brown Sugar Mix Powder No. 1', 'supplier': 'Kingleke', 'quantity': 8, 'price': 22.50, 'unit': '2kg bag'},
            {'name': 'Original Coconut Jelly', 'supplier': 'Kingleke', 'quantity': 12, 'price': 12.75, 'unit': '500g container'},
            {'name': 'Mix Coconut Jelly', 'supplier': 'Kingleke', 'quantity': 10, 'price': 12.75, 'unit': '500g container'},
            {'name': 'Lychee Coconut Jelly', 'supplier': 'Kingleke', 'quantity': 8, 'price': 13.25, 'unit': '500g container'},
            {'name': 'Cane Liquid Sugar', 'supplier': 'Kingleke', 'quantity': 6, 'price': 18.50, 'unit': '2L bottle'},
            {'name': 'Jasmine Green Tea', 'supplier': 'Kingleke', 'quantity': 8, 'price': 16.99, 'unit': '1kg bag'},
            {'name': 'Honey Dew Powder', 'supplier': 'Kingleke', 'quantity': 5, 'price': 24.99, 'unit': '1kg bag'},
            {'name': 'Mango Powder', 'supplier': 'Kingleke', 'quantity': 6, 'price': 26.99, 'unit': '1kg bag'},
            {'name': 'Kesar Mango Pulp', 'supplier': 'Kingleke', 'quantity': 8, 'price': 8.99, 'unit': '850g can'},
            {'name': 'Matcha Latte Powder', 'supplier': 'Kingleke', 'quantity': 4, 'price': 32.99, 'unit': '1kg bag'},
            {'name': 'Cookies & Cream Powder', 'supplier': 'Kingleke', 'quantity': 3, 'price': 28.99, 'unit': '1kg bag'},
            {'name': 'Strawberry Powder', 'supplier': 'Kingleke', 'quantity': 5, 'price': 25.99, 'unit': '1kg bag'},
            {'name': 'Tapioca Pearls', 'supplier': 'Kingleke', 'quantity': 6, 'price': 14.99, 'unit': '3kg bag'},
            {'name': 'Taro Powder', 'supplier': 'Kingleke', 'quantity': 4, 'price': 27.99, 'unit': '1kg bag'},
            {'name': 'Thai Tea Mix', 'supplier': 'Kingleke', 'quantity': 5, 'price': 19.99, 'unit': '1kg bag'},
            {'name': 'Bubble Tea Wrapped-Plastic Straw', 'supplier': 'Kingleke', 'quantity': 15, 'price': 12.00, 'unit': '1000 pack'},

            # QualiTea Products
            {'name': 'Brown Sugar Syrup', 'supplier': 'QualiTea', 'quantity': 8, 'price': 16.99, 'unit': '2.5kg bottle'},
            {'name': 'Mango Coating Juice Ball', 'supplier': 'QualiTea', 'quantity': 6, 'price': 15.99, 'unit': '3.2kg jar'},
            {'name': 'Mango Syrup', 'supplier': 'QualiTea', 'quantity': 5, 'price': 14.99, 'unit': '2.5kg bottle'},
            {'name': 'Passion Fruit Syrup', 'supplier': 'QualiTea', 'quantity': 4, 'price': 16.99, 'unit': '2.5kg bottle'},
            {'name': 'Passion Fruit Powder', 'supplier': 'QualiTea', 'quantity': 3, 'price': 29.99, 'unit': '1kg bag'},
            {'name': 'Peach Syrup', 'supplier': 'QualiTea', 'quantity': 6, 'price': 15.99, 'unit': '2.5kg bottle'},
            {'name': 'Coconut Powder', 'supplier': 'QualiTea', 'quantity': 4, 'price': 23.99, 'unit': '1kg bag'},
            {'name': 'Strawberry Coating Juice Ball', 'supplier': 'QualiTea', 'quantity': 8, 'price': 15.99, 'unit': '3.2kg jar'},
            {'name': 'Lychee Syrup', 'supplier': 'QualiTea', 'quantity': 5, 'price': 17.99, 'unit': '2.5kg bottle'},
            {'name': '500CC PC Shaker', 'supplier': 'QualiTea', 'quantity': 4, 'price': 8.99, 'unit': 'each'},
            {'name': '700CC PC Shaker', 'supplier': 'QualiTea', 'quantity': 3, 'price': 10.99, 'unit': 'each'},
            {'name': 'Tapioca Scooper', 'supplier': 'QualiTea', 'quantity': 5, 'price': 5.99, 'unit': 'each'},
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                supplier=product_data['supplier'],
                defaults={
                    'quantity': product_data['quantity'],
                    'restock_threshold': 1,  # All products start with threshold of 1
                    'price': product_data['price'],
                    'unit': product_data['unit'],
                    'description': f"{product_data['name']} from {product_data['supplier']}"
                }
            )
            if created:
                self.stdout.write(f'✅ Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully seeded Boba Stop inventory data!')
        )