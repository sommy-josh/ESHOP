from rest_framework import serializers
from .models import Product,Review,Cart,CartItem,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','description', 'price']

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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    orderitems=serializers.SerializerMethodField(method_name='get_order_items',read_only=True)
    class Meta:
        model=Order
        fields="__all__"
    def get_order_items(self, obj):
        order_items=obj.orderitems.all()
        serializer=OrderItemSerializer(order_items,many=True)
        return serializer.data

