from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ProductImageViewSet, ProductVarientViewSet,
    ProductDetailView  # Add this import
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-variants', ProductVarientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Add product detail URL
]