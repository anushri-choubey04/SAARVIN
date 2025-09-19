from django.contrib import admin
from .models import Rental, RentalItem, Payment, Delivery, Cart


class RentalItemInline(admin.TabularInline):
    model = RentalItem
    extra = 0


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('rental_id', 'renter', 'product', 'start_date', 'end_date', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'created_at')
    search_fields = ('rental_id', 'renter__username', 'product__name')
    raw_id_fields = ('renter', 'product')
    inlines = [RentalItemInline]


@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ('rental', 'product', 'quantity', 'daily_rate', 'total_amount')
    raw_id_fields = ('rental', 'product')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('rental', 'amount', 'payment_method', 'payment_status', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('rental__rental_id', 'transaction_id')
    raw_id_fields = ('rental',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('rental', 'status', 'tracking_number', 'delivery_agent', 'estimated_delivery', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('rental__rental_id', 'tracking_number', 'delivery_agent')
    raw_id_fields = ('rental',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'start_date', 'end_date', 'quantity', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    raw_id_fields = ('user', 'product')
