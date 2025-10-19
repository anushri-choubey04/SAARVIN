from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model for SAARVIN RENT"""
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Additional user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], blank=True, null=True)
    preferred_size = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Wishlist(models.Model):
    """Wishlist model to store user's favorite products"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product_id = models.IntegerField()  # Assuming product IDs are integers
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_id')

    def __str__(self):
        return f"Wishlist of {self.user.username} - Product ID: {self.product_id}"
    

class Cart(models.Model):
    """Shopping cart model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product_id = models.IntegerField()  # Assuming product IDs are integers
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_id')

    def __str__(self):
        return f"Cart of {self.user.username} - Product ID: {self.product_id} (Qty: {self.quantity})"


class Order(models.Model):
    """Order model to store user orders"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=20, unique=True)
    product_id = models.IntegerField()  # Assuming product IDs are integers
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned')
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
    
