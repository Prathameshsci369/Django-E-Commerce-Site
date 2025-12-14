from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVarient, ProductReview  # Use ProductVarient

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'is_active', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'sort_order', 'created_at']

class ProductVarientSerializer(serializers.ModelSerializer):  # Use ProductVarientSerializer
    class Meta:
        model = ProductVarient  # Use ProductVarient
        fields = ['id', 'name', 'value', 'price_adjustment', 'quantity', 'created_at']

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'title', 'content', 'is_verified', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVarientSerializer(many=True, read_only=True)  # Use ProductVarientSerializer
    reviews = ProductReviewSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_price',
            'sku', 'track_quantity', 'quantity', 'weight', 'is_active',
            'is_featured', 'category', 'images', 'variants', 'reviews',
            'discount_percentage', 'primary_image', 'created_at', 'updated_at'
        ]

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()

    def get_primary_image(self, obj):
        primary_image = obj.get_primary_image()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'compare_price', 'sku',
            'quantity', 'is_featured', 'category', 'primary_image',
            'discount_percentage'
        ]

    def get_primary_image(self, obj):
        primary_image = obj.get_primary_image()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()