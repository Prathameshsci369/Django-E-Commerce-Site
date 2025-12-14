from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email= models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email 
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    address_type = models.CharField(max_length=10,choices=[
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
    ],default='shipping')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100,blank=True)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    phone = models.CharField(max_length=20,blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Addresses'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"
    
    





