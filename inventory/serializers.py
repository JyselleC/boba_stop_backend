from rest_framework import serializers
from .models import Product, Supplier, ActivityLog

class ProductSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'quantity', 'restock_threshold', 
                 'price', 'unit', 'supplier', 'status', 'last_updated']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'address', 'phone', 'email', 'website', 'description']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'details', 'timestamp']