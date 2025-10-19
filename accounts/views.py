from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import json

from accounts.models import Order
from products.models import Wishlist
from rentals.models import Cart

User = get_user_model()


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password:
            # Try to authenticate with username first
            user = authenticate(request, username=username, password=password)
            
            # If that fails, try to authenticate with email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get("next", "home")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password")
        else:
            messages.error(request, "Please fill in all fields")
    return render(request, "login.html")
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'register.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.pincode = request.POST.get('pincode', user.pincode)
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html')


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """API login endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """API registration endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone = data.get('phone', '')
        
        if not all([username, email, password]):
            return JsonResponse({'error': 'Username, email and password required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        login(request, user)
        return JsonResponse({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """API logout endpoint"""
    logout(request)
    return JsonResponse({'message': 'Logout successful'})




@login_required
def cart_view(request):
    """User cart view"""
    carts = request.user.carts.all()
    return render(request, 'cart.html', {'carts': carts})
@csrf_exempt
@login_required

def api_cart(request):
    """API cart endpoint"""
    if request.method == 'GET':
        carts = request.user.carts.all()
        cart_list = [{
            'product_id': cart.product_id,
            'quantity': cart.quantity,
            'added_at': cart.added_at
        } for cart in carts]
        return JsonResponse({'cart': cart_list})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            if not product_id:
                return JsonResponse({'error': 'Product ID required'}, status=400)
            
            cart, created = request.user.carts.get_or_create(product_id=product_id)
            if not created:
                cart.quantity += quantity
            else:
                cart.quantity = quantity
            cart.save()
            
            return JsonResponse({
                'message': 'Product added to cart',
                'cart': {
                    'product_id': cart.product_id,
                    'quantity': cart.quantity,
                    'added_at': cart.added_at
                }
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if not product_id:
                return JsonResponse({'error': 'Product ID required'}, status=400)
            
            try:
                cart = request.user.carts.get(product_id=product_id)
                cart.delete()
                return JsonResponse({'message': 'Product removed from cart'})
            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Product not in cart'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)@csrf_exempt
@login_required
def api_profile(request):
    """API profile endpoint"""
    user = request.user
    if request.method == 'GET':
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'address': user.address,
            'city': user.city,
            'pincode': user.pincode,
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.phone = data.get('phone', user.phone)
            user.address = data.get('address', user.address)
            user.city = data.get('city', user.city)
            user.pincode = data.get('pincode', user.pincode)
            user.save()
            
            return JsonResponse({'message': 'Profile updated successfully'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)@csrf_exempt
@login_required
def api_orders(request):
    """API orders endpoint"""
    # Placeholder implementation
    if request.method == 'GET':
        orders = []  # Replace with actual order retrieval logic
        return JsonResponse({'orders': orders})
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)@csrf_exempt
@login_required 
def api_wishlist(request):
    """API wishlist endpoint"""
    if request.method == 'GET':
        wishlists = request.user.wishlists.all()
        wishlist_list = [{
            'product_id': wishlist.product_id,
            'added_at': wishlist.added_at
        } for wishlist in wishlists]
        return JsonResponse({'wishlist': wishlist_list})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if not product_id:
                return JsonResponse({'error': 'Product ID required'}, status=400)
            
            wishlist, created = request.user.wishlists.get_or_create(product_id=product_id)
            if created:
                return JsonResponse({
                    'message': 'Product added to wishlist',
                    'wishlist': {
                        'product_id': wishlist.product_id,
                        'added_at': wishlist.added_at
                    }
                })
            else:
                return JsonResponse({'message': 'Product already in wishlist'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if not product_id:
                return JsonResponse({'error': 'Product ID required'}, status=400)
            
            try:
                wishlist = request.user.wishlists.get(product_id=product_id)
                wishlist.delete()
                return JsonResponse({'message': 'Product removed from wishlist'})
            except Wishlist.DoesNotExist:
                return JsonResponse({'error': 'Product not in wishlist'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
@login_required
def wishlist_view(request):
    """User wishlist view"""
    wishlists = request.user.wishlists.all()
    return render(request, 'wishlist.html', {'wishlists': wishlists})
@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    wishlist, created = request.user.wishlists.get_or_create(product_id=product_id)
    if created:
        messages.success(request, 'Product added to wishlist')
    else:
        messages.info(request, 'Product already in wishlist')
    return redirect('wishlist')
@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    try:
        wishlist = request.user.wishlists.get(product_id=product_id)
        wishlist.delete()
        messages.success(request, 'Product removed from wishlist')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Product not in wishlist')
    return redirect('wishlist')
@login_required
def orders_view(request):
    """User orders view"""
    orders = request.user.orders.all()
    return render(request, 'orders.html', {'orders': orders})
@login_required
def order_detail(request, order_id):
    """Order detail view"""
    try:
        order = request.user.orders.get(order_id=order_id)
        return render(request, 'order_detail.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('orders')
@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    try:
        order = request.user.orders.get(order_id=order_id)
        if order.status == 'Pending':
            order.status = 'Cancelled'
            order.save()
            messages.success(request, 'Order cancelled successfully')
        else:
            messages.error(request, 'Only pending orders can be cancelled')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
    return redirect('orders')
@login_required
def return_order(request, order_id):
    """Return an order"""
    try:
        order = request.user.orders.get(order_id=order_id)
        if order.status == 'Delivered':
            order.status = 'Returned'
            order.save()
            messages.success(request, 'Order return initiated successfully')
        else:
            messages.error(request, 'Only delivered orders can be returned')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
    return redirect('orders')
@login_required
def review_order(request, order_id):
    """Review an order"""
    try:
        order = request.user.orders.get(order_id=order_id)
        if request.method == 'POST':
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            # Placeholder: Save review and rating logic here
            messages.success(request, 'Thank you for your review!')
            return redirect('orders')
        return render(request, 'review_order.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('orders')
from django.db import models
from django.contrib.auth.models import AbstractUser
