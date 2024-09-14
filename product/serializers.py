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
        fields=['id', 'quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id', 'user','created_at' 'total_price','status', 'items']

        def create(self, validated_data):
            items_data=validated_data.pop('items')
            order=Order.objects.create(**validated_data)
            total_price=0
            
            for item_data in items_data:
                product=item_data['product']
                quantity=item_data['quantity']
                price=product.price *quantity
                total_price +=price

                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

                #reduce stock
                product.stock -= quantity
                product.save()

            order.total_price =total_price
            order.save()
            return order
