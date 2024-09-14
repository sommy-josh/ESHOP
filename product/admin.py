from django.contrib import admin
from .models import Product,CartItem,Cart,Review

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
