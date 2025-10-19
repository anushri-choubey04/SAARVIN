from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/return/', views.return_order, name='return_order'),
    path('orders/<int:order_id>/review/', views.review_order, name='review_order'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    

    
    # API endpoints
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/cart/', views.api_cart, name='api_cart'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/wishlist/', views.api_wishlist, name='api_wishlist'),

]
