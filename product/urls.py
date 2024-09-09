from django.urls import path
from .views import CartView,RemoveCartItemView
from . import views

urlpatterns=[
    path('products/',  views.get_product, name='get-product'),
    path('products/<str:pk>/', views.get_product_detail, name='get-product'),

    
    # add to cart= POST domain/api/cart/
    # view cart=GET domain/api/cart
    # update cart=PATCH domain/api/cart
    # delete the cart= DELETE domain/api/cart/item/id/remove


    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
]