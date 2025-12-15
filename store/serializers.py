from .models import Product , Customer , Order , OrderItem
from rest_framework import serializers 
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
        
        
        
        
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    name = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email','name']
        read_only_fields = ['username', 'email','name']
        
    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
        
        
        
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    
    product_details = ProductSerializer(source ='product' , read_only=True)
    
    #  Custom field to calculate the total price for this line item
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        # Note: 'product' is included for creating the OrderItem (POST request)
        fields =['id', 'product', 'quantity', 'total_price','product_details']
        
    # Calculates the subtotal for the item (Quantity * Product Price)
    def get_total_price(self, obj):
        return obj.get_total
    
    
    
    
    
class OrderSerializer(serializers.ModelSerializer):
    customer_info = CustomerSerializer(source='customer', read_only=True)

    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    
    # Custom field for the overall grand total
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 
            'customer',        # FK ID (for writing/updates)
            'customer_info',   # Nested details (for reading)
            'date_ordered', 
            'status', 
            'transaction_id', 
            'complete',
            'items',           # Nested order items
            'grand_total'
        ]

    def get_grand_total(self, obj):
        # Calculates the sum of all item totals linked to this order
        total = sum(item.get_total for item in obj.orderitem_set.all())
        return total