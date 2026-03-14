import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_site.settings')
import django
django.setup()
from shop.models import Product

products = Product.objects.all().order_by('id')
if not products.exists():
    print('No products found')
else:
    for p in products:
        print(f"{p.id}\t{p.name}\t{p.price}\t{p.description}")
