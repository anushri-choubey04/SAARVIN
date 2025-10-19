
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'ProductDetails.html', {'product': product})

