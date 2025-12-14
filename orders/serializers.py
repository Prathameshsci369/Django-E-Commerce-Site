from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from accounts.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'subtotal', 'tax', 'shipping',
            'total', 'shipping_address', 'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'user']