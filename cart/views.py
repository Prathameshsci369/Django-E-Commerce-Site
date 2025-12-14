from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
            if product.track_quantity and product.quantity < quantity:
                return Response(
                    {'error': 'Insufficient stock'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            if quantity <= 0:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
            
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'message': 'Cart updated'})
            
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return CartItem.objects.filter(cart=cart)