from django.contrib import admin
from .models import Product,CartItem,Cart

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
