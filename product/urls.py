from django.urls import path
from .views import CartView,RemoveCartItemView,OrderCreateView,OrderDetailView
from . import views

urlpatterns=[
    path('products/',  views.get_product, name='get-product'),
    path('products/<str:pk>/', views.get_product_detail, name='get-product'),
    path('create_product/', views.create_product, name='create-product'),
    path('update_product/<str:id>/', views.update_product, name='update-product'),
    path('delete_product/<str:id>/',views.delete_product, name='delete-product'),
    path('create_review/<str:product_id>/', views.review_create, name="review-create"),
    path('list_review/', views.review_list, name='review-list'),
    path('update_review/<str:pk>/', views.update_review, name='update-review'),
    path('delete_review/<str:pk>/', views.delete_review,  name='delete-review'),
    
    # add to cart= POST domain/api/cart/
    # view cart=GET domain/api/cart
    # update cart=PATCH domain/api/cart
    # delete the cart= DELETE domain/api/cart/item/id/remove


    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]