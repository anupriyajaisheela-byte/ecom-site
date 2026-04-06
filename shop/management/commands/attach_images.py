from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from pathlib import Path

from shop.models import Product


class Command(BaseCommand):
    help = 'Attach images from MEDIA_ROOT/products to Product.image when names match'

    def handle(self, *args, **options):
        media_products = Path(settings.MEDIA_ROOT) / 'products'
        if not media_products.exists():
            self.stdout.write(self.style.ERROR(f"Media folder not found: {media_products}"))
            return

        files = sorted([p for p in media_products.iterdir() if p.is_file()])
        if not files:
            self.stdout.write(self.style.WARNING('No image files found in media/products'))
            return

        updated = 0
        for f in files:
            stem = f.stem.lower()
            try:
                prod = Product.objects.get(name__iexact=stem)
            except Product.DoesNotExist:
                self.stdout.write(self.style.NOTICE(f'No product matching: {stem}'))
                continue

            if prod.image:
                self.stdout.write(self.style.WARNING(f'{prod.name} already has an image; skipping'))
                continue

            with open(f, 'rb') as fh:
                prod.image.save(f.name, File(fh), save=True)
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Attached {f.name} to {prod.name}'))

        self.stdout.write(self.style.SUCCESS(f'Finished — updated {updated} products.'))
