from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    
    # API endpoints
    path('api/newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/clear/', views.clear_cart, name='clear_cart'),
    path('api/search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
