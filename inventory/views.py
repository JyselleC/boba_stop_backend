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
    
    @action(detail=False, methods=['post'])
    def send_low_stock_alert(self, request):
        """Send SMS alert for low stock items to multiple recipients"""
        try:
            # Get low stock products
            low_stock_products = Product.objects.filter(
                quantity__lte=F('restock_threshold')
            )
            
            if not low_stock_products.exists():
                return Response({'message': 'No low stock items found'})
            
            # Create alert message
            product_names = [p.name for p in low_stock_products[:5]]  # Limit to 5 items
            message = f"🧋 Boba Stop Alert: Low stock items: {', '.join(product_names)}"
            if low_stock_products.count() > 5:
                message += f" and {low_stock_products.count() - 5} more items."
            
            # Send SMS using Twilio to all recipients
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            results = []
            for recipient in settings.SMS_RECIPIENTS:
                if recipient:  # Only send if recipient is not empty
                    try:
                        twilio_message = client.messages.create(
                            body=message,
                            from_=settings.TWILIO_PHONE_NUMBER,
                            to=recipient
                        )
                        results.append({
                            'recipient': recipient,
                            'status': 'sent',
                            'sid': twilio_message.sid
                        })
                    except Exception as e:
                        results.append({
                            'recipient': recipient,
                            'status': 'failed',
                            'error': str(e)
                        })
            
            return Response({
                'message': f'Alerts sent to {len([r for r in results if r["status"] == "sent"])} recipients',
                'items_count': low_stock_products.count(),
                'results': results
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to send alert: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
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