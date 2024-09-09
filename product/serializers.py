from rest_framework import serializers
from .models import Product,Review,Cart,CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model=CartItem
        fields=['id','product', 'product_name', 'price', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    class Meta:
        model=Cart
        fields=['id','user','items','created_at']