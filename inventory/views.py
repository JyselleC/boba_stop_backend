from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, F
from .models import Product, Supplier, ActivityLog
from .serializers import ProductSerializer, SupplierSerializer, ActivityLogSerializer
from twilio.rest import Client
from django.conf import settings

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def suppliers(self, request):
        """Get all unique suppliers"""
        suppliers = Product.objects.values_list('supplier', flat=True).distinct().order_by('supplier')
        return Response(list(suppliers))
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock"""
        low_stock_products = Product.objects.filter(
            quantity__lte=F('restock_threshold')
        ).order_by('name')
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get inventory statistics"""
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(
            quantity__lte=F('restock_threshold')
        ).count()
        out_of_stock_count = Product.objects.filter(quantity=0).count()
        suppliers_count = Product.objects.values('supplier').distinct().count()
        
        return Response({
            'total_products': total_products,
            'low_stock_items': low_stock_count,
            'out_of_stock_items': out_of_stock_count,
            'suppliers_count': suppliers_count
        })

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('name')
    serializer_class = SupplierSerializer

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    http_method_names = ['get', 'post']  # Only allow GET and POST
    
    def get_queryset(self):
        queryset = ActivityLog.objects.all()
        user = self.request.query_params.get('user', None)
        action = self.request.query_params.get('action', None)
        
        if user:
            queryset = queryset.filter(user__icontains=user)
        if action:
            queryset = queryset.filter(action=action)
            
        return queryset[:1000]  # Limit to last 1000 logs