from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import Category, Product, ProductImage, ProductVarient, ProductReview
from .serializers import (
    CategorySerializer, ProductSerializer, ProductListSerializer,
    ProductImageSerializer, ProductVarientSerializer, ProductReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)  # Added queryset attribute
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        category = self.get_object()
        products = category.products.filter(is_active=True)
        page = self.paginate_queryset(products)
        serializer = ProductListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Manual filtering (instead of DjangoFilterBackend)
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')

        if category:
            queryset = queryset.filter(category__slug=category)
        
        if featured and featured.lower() in ['true', '1']:
            queryset = queryset.filter(is_featured=True)
        elif featured and featured.lower() in ['false', '0']:
            queryset = queryset.filter(is_featured=False)
        
        return queryset

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        serializer = ProductListSerializer(related_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, slug=None):
        product = self.get_object()
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()  # Added queryset attribute
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductVarientViewSet(viewsets.ModelViewSet):
    queryset = ProductVarient.objects.all()  # Added queryset attribute
    serializer_class = ProductVarientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products
        product = self.get_object()
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        return context