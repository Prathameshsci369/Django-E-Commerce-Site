from django.db import models
from django.contrib.auth import get_user_model 
from products.models import Product 

User = get_user_model() 

class  Cart(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True )

    def __str__(self):
        return f"{self.user.username}'s cart"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.item.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ( 'cart', 'product') 

    def __str__(self):
        return f"{self.product.name} - "

    def get_total_price(self):
        return self.product.price * self.quantity
    
    