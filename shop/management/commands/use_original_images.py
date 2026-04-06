from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path

from shop.models import Product


class Command(BaseCommand):
    help = 'Use existing media/products/<name>.jpg for Product.image and remove hashed duplicates'

    def handle(self, *args, **options):
        media_products = Path(settings.MEDIA_ROOT) / 'products'
        if not media_products.exists():
            self.stdout.write(self.style.ERROR(f"Media folder not found: {media_products}"))
            return

        changed = 0
        removed = 0
        for prod in Product.objects.all():
            base_name = prod.name.lower()
            desired = media_products / f"{base_name}.jpg"

            if desired.exists():
                # point ImageField to the original file name
                new_name = f"products/{desired.name.split('products' + Path('/').as_posix())[-1]}" if 'products' in desired.as_posix() else f"products/{desired.name}"
                # simpler: set to products/<base_name>.jpg
                prod.image.name = f"products/{base_name}.jpg"
                prod.save()
                changed += 1

                # remove any hashed variants like name_*.jpg
                for p in media_products.iterdir():
                    if not p.is_file():
                        continue
                    stem = p.stem
                    if stem.startswith(base_name + '_'):
                        try:
                            p.unlink()
                            removed += 1
                            self.stdout.write(self.style.SUCCESS(f'Removed hashed file {p.name}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Failed to remove {p.name}: {e}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Original file not found for {prod.name}: expected {desired.name}'))

        self.stdout.write(self.style.SUCCESS(f'Updated {changed} products. Removed {removed} hashed files.'))
