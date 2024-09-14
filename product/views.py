from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import ProductsFilter
from rest_framework import status
from .serializers import CartSerializer, CartItemSerializer,OrderItemSerializer,OrderSerializer,ReviewSerializer
from .serializers import ProductSerializer
from .models import Product,CartItem,Cart,Order,OrderItem,Review
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions



# Create your views here.
@api_view(['GET'])
def get_product(request):
    # filtering the products and ordering them by the id
    filterset=ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))

    # counting the number of all the product
    count=filterset.qs.count()
    
    # how many result to have in a page
    resPerPage=5
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

@api_view(['POST'])
def create_product(request):
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "products created successfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_product(request,id):
    try:
        product=Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"message": "product Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer=ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.error)


@api_view(['DELETE'])
def delete_product(request,id):
    try:
        product=Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response("Product Not Found", status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({"message": "product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

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


class OrderCreateView(generics.CreateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create(request,product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"message": "Product Not Found"})
    serializer=ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def review_list(request):
        reviews=Review.objects.all()
        serializer=ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, pk):
    try:
        review=Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response({"message": "Review Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    if review.user !=request.user:
        return Response({"message": "you are not authorized to update this review"}, status=status.HTTP_403_FORBIDDEN)
    serializer=ReviewSerializer(review, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    try:
        review=Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response("Review not found", status=status.HTTP_404_NOT_FOUND)
    if review.user != request.user:
        return Response({"message": " you are not authorized to delete this review"})
    review.delete()
    return Response({"message":"Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
