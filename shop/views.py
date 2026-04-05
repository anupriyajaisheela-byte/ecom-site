from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Product, CartItem
from django.conf import settings
import json


def _get_session_key(request):
    # ensure session exists and return key
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def products(request):
    prods = Product.objects.all()
    data = []
    for p in prods:
        # We manually point to the folder where your images are stored
        # Change 'media/' to 'static/' if your images are in the static folder
        image_path = f"{settings.MEDIA_URL}{p.name.lower()}.jpg" 
        
        data.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'image': image_path  # This uses the file already in your project
        })
    return JsonResponse(data, safe=False)


def get_cart(request):
    session_key = _get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)
    items_data = [{'id': i.id, 'product_id': i.product.id, 'name': i.product.name, 'price': i.product.price, 'quantity': i.quantity} for i in items]
    total = sum(i['price'] * i['quantity'] for i in items_data)
    return JsonResponse({'items': items_data, 'total': total})


@csrf_exempt
def add_to_cart(request):
    data = json.loads(request.body.decode() or '{}')
    product_id = data.get('product_id')
    qty = int(data.get('quantity', 1))
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'product not found'}, status=404)
    session_key = _get_session_key(request)
    item, created = CartItem.objects.get_or_create(product=p, session_key=session_key)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def remove_from_cart(request):
    data = json.loads(request.body.decode() or '{}')
    product_id = data.get('product_id')
    qty = int(data.get('quantity', 1))
    session_key = _get_session_key(request)
    try:
        item = CartItem.objects.get(product__id=product_id, session_key=session_key)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'item not in cart'}, status=404)
    item.quantity -= qty
    if item.quantity <= 0:
        item.delete()
    else:
        item.save()
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def checkout(request):
    session_key = _get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)
    summary = {
        'items': [{'name': i.product.name, 'price': i.product.price, 'quantity': i.quantity} for i in items],
        'total': sum(i.product.price * i.quantity for i in items),
        'timestamp': timezone.now().isoformat()
    }
    items.delete()
    return JsonResponse({'status': 'confirmed', 'summary': summary})
