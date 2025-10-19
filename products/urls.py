from django.urls import path
from . import views

urlpatterns = [
    
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Product API endpoints will be added here
]
