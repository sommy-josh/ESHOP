from django.urls import path
from . import views

urlpatterns=[
    path('products/',  views.get_product, name='get-product'),
    path('products/<str:pk>/', views.get_product_detail, name='get-product'),
]