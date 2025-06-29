from django.contrib import admin
from .models import Product, Supplier, ActivityLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'quantity', 'restock_threshold', 'status', 'price', 'last_updated']
    list_filter = ['supplier', 'created_at']
    search_fields = ['name', 'supplier']
    ordering = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['name']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'details', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user', 'details']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']