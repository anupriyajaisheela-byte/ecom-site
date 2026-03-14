from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Seed initial products into the database (if none exist)'

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Products already exist — skipping seeding.'))
            return

        items = [
{'name': 'Apple', 'price': 0.5, 'description': 'Fresh red apple', 'image': 'products/apple.jpg'}
{'name': 'Banana', 'price': 0.3, 'description': 'Ripe banana', 'image': 'products/banana.jpg'}
{'name': 'Orange', 'price': 0.6, 'description': 'Juicy orange', 'image': 'products/orange.jpg'}
{'name': 'Grapes', 'price': 2.5, 'description': 'Seedless grapes (per bunch)', 'image': 'products/grapes.jpg'}
{'name': 'Mango', 'price': 1.5, 'description': 'Sweet mango', 'image': 'products/mango.jpg'}
        ]

        for it in items:
Product.objects.create(**it)

        self.stdout.write(self.style.SUCCESS(f'Created {len(items)} products.'))
