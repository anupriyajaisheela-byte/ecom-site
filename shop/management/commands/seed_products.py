from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Seed initial products into the database (use --force to recreate)'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Delete existing products and recreate')

    def handle(self, *args, **options):
        force = options.get('force')
        if Product.objects.exists() and not force:
            self.stdout.write(self.style.WARNING('Products already exist — skipping seeding. Use --force to recreate.'))
            return

        if force:
            Product.objects.all().delete()

        items = [
            {'name': 'Apple', 'price': 0.5, 'description': 'Fresh red apple'},
            {'name': 'Banana', 'price': 0.3, 'description': 'Ripe banana'},
            {'name': 'Orange', 'price': 0.6, 'description': 'Juicy orange'},
            {'name': 'Grapes', 'price': 2.5, 'description': 'Seedless grapes (per bunch)'},
            {'name': 'Mango', 'price': 1.5, 'description': 'Sweet mango'},
        ]

        created = 0
        for it in items:
            Product.objects.create(**it)
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} products.'))
