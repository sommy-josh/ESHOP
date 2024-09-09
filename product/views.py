from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import ProductsFilter
from rest_framework import status
from .serializers import CartSerializer, CartItemSerializer
from .serializers import ProductSerializer
from .models import Product,CartItem,Cart
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# Create your views here.
@api_view(['GET'])
def get_product(request):
    # filtering the products and ordering them by the id
    filterset=ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))

    # counting the number of all the product
    count=filterset.qs.count()
    
    # how many result to have in a page
    resPerPage=1
    paginator=PageNumberPagination()
    paginator.page_size=resPerPage
    queryset=paginator.paginate_queryset(filterset.qs, request)
    serializer=ProductSerializer(queryset, many=True)

    return Response({"count":count, "resPerPage":resPerPage, "product": serializer.data,  })

@api_view(['GET'])
def get_product_detail(request,pk):
    product=get_object_or_404(Product,id=pk)
    serializer=ProductSerializer(product, many=False)
    return Response({'product':serializer.data},status=status.HTTP_200_OK)










class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += int(quantity)

        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

class RemoveCartItemView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            return Response({"message": "product deleted successfully from the cart"},status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
