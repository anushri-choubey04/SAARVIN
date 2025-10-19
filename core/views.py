from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import Banner, FAQ, Story, Contact, Newsletter
from products.models import Product, Category, SubCategory, Wishlist
from rentals.models import Cart


def home(request):
    """Homepage view"""
    # Get featured products
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    
    # Get categories
    categories = Category.objects.filter(is_active=True)[:7]
    
    # Get banners
    banners = Banner.objects.filter(is_active=True).exclude(image="").exclude(image__isnull=True).order_by("order")
    
    # Get stories
    stories = Story.objects.filter(is_active=True)[:10]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'banners': banners,
        'stories': stories,
    }
    return render(request, 'index.html', context)


def shop(request):
    """Shop page view"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filtering
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    size = request.GET.get('size')
    
    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(brand__icontains=search)
        )
    if min_price:
        products = products.filter(rental_price_per_day__gte=min_price)
    if max_price:
        products = products.filter(rental_price_per_day__lte=max_price)
    if size:
        products = products.filter(size=size)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_id,
        'current_subcategory': subcategory_id,
        'search_query': search,
    }
    return render(request, 'shop.html', context)


def product_detail(request, product_id):
    """Product detail view"""
    try:
        product = Product.objects.get(id=product_id, is_available=True)
        related_products = Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product_id)[:4]
        
        # Check if product is in user's wishlist
        in_wishlist = False
        if request.user.is_authenticated:
            in_wishlist = Wishlist.objects.filter(
                user=request.user, 
                product=product
            ).exists()
        
        context = {
            'product': product,
            'related_products': related_products,
            'in_wishlist': in_wishlist,
        }
        return render(request, 'product_detail.html', context)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('shop')


@login_required
def wishlist(request):
    """User wishlist view"""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)


@login_required
def cart(request):
    """Shopping cart view"""
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_amount for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart.html', context)


def faq(request):
    """FAQ page view"""
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    context = {
        'faqs': faqs,
    }
    return render(request, 'faq.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    
    return render(request, 'contact.html')


# API Views
@csrf_exempt
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription API"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        
        if created:
            return JsonResponse({'message': 'Successfully subscribed to newsletter'})
        else:
            return JsonResponse({'message': 'Email already subscribed'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_to_wishlist(request):
    """Add product to wishlist API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        
        product = Product.objects.get(id=product_id, is_available=True)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            return JsonResponse({'message': 'Added to wishlist'})
        else:
            return JsonResponse({'message': 'Already in wishlist'})
    
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def remove_from_wishlist(request):
    """Remove product from wishlist API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        return JsonResponse({'message': 'Removed from wishlist'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    """Add product to cart API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        quantity = data.get('quantity', 1)
        
        if not all([product_id, start_date, end_date]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        product = Product.objects.get(id=product_id, is_available=True)
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            start_date=start_date,
            end_date=end_date,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'message': 'Added to cart'})
    
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def search_suggestions(request):
    """Search suggestions API"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Search in product names and categories
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(brand__icontains=query)
    )[:5]
    
    categories = Category.objects.filter(
        name__icontains=query
    )[:3]
    
    suggestions = []
    for product in products:
        suggestions.append({
            'type': 'product',
            'name': product.name,
            'url': f'/product/{product.id}/'
        })
    
    for category in categories:
        suggestions.append({
            'type': 'category',
            'name': category.name,
            'url': f'/shop/?category={category.id}'
        })
    
    return JsonResponse({'suggestions': suggestions})


@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove item from cart API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        
        if not cart_item_id:
            return JsonResponse({'error': 'Cart item ID is required'}, status=400)
        
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        
        return JsonResponse({'message': 'Item removed from cart'})
    
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        Cart.objects.filter(user=request.user).delete()
        return JsonResponse({'message': 'Cart cleared successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


