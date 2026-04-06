from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Check database connectivity for the default database.'

    def handle(self, *args, **options):
        self.stdout.write('Checking default database connection...')
        conn = connections['default']
        try:
            # Try a simple operation
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                result = cur.fetchone()
            self.stdout.write(self.style.SUCCESS(f'Database OK: {result}'))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR('Database connection failed:'))
            self.stdout.write(str(e))
            raise SystemExit(1)
