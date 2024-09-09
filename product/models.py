from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.TextChoices):
    ELECTRONICS='Electronics'
    LAPTOPS='Laptops'
    ARTS='Arts'
    FOOD='Food'
    HOME='Home'
    KITCHEN='Kitchen'




class Product(models.Model):
    name=models.CharField(max_length=200,default="", blank=False)
    description=models.TextField(max_length=1000,default="", blank=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand=models.CharField(max_length=200, default="", blank=False)
    category=models.CharField(max_length=30, choices=Category.choices)
    ratings=models.DecimalField(max_digits=3,decimal_places=2, default=0)
    stock=models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating=models.IntegerField(default=0)
    comment=models.TextField(default="", blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)


class Cart(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='product_cart')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' cart for {self.user.username}'

class CartItem(models.Model):
    cart=models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"