from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import ProductsFilter
from rest_framework import status

from .serializers import ProductSerializer
from .models import Product

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



