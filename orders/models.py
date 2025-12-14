from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product 

User = get_user_model() 

class Order(models.Model):
    STATUS_CHOICE = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE,default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places = 2)
    tax = models.DecimalField(max_digits=10,decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True, blank=True) 
    notes = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"Order {self.order_number} "
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid 
            self.order_number  = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total = self.price* self.quantity
        super().save(*args, **kwargs)