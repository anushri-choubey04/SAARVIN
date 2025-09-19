from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Rental(models.Model):
    """Rental transactions"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PICKED_UP', 'Picked Up'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    # Basic Information
    rental_id = models.CharField(max_length=20, unique=True)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rentals')
    
    # Rental Details
    start_date = models.DateField()
    end_date = models.DateField()
    rental_days = models.PositiveIntegerField()
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Delivery Information
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_pincode = models.CharField(max_length=10)
    delivery_phone = models.CharField(max_length=15)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rental {self.rental_id} - {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.rental_id:
            # Generate rental ID
            import uuid
            self.rental_id = f"RENT{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class RentalItem(models.Model):
    """Individual items in a rental (for future multi-item rentals)"""
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.rental.rental_id} - {self.product.name}"


class Payment(models.Model):
    """Payment records for rentals"""
    PAYMENT_METHOD_CHOICES = [
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NET_BANKING', 'Net Banking'),
        ('WALLET', 'Wallet'),
        ('COD', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_gateway_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.rental.rental_id} - {self.amount}"


class Delivery(models.Model):
    """Delivery tracking for rentals"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('RETURN_PENDING', 'Return Pending'),
        ('RETURNED', 'Returned'),
    ]

    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    delivery_agent = models.CharField(max_length=100, blank=True, null=True)
    delivery_phone = models.CharField(max_length=15, blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    actual_delivery = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for {self.rental.rental_id} - {self.status}"


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product', 'start_date', 'end_date']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_amount(self):
        return self.product.rental_price_per_day * self.total_days * self.quantity
