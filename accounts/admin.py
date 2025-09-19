from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_verified', 'is_staff', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'city', 'pincode', 'profile_picture', 'is_verified')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'preferred_size', 'date_of_birth')
    list_filter = ('gender', 'preferred_size')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
