from django.db import models
from django.contrib.auth import get_user_model 
from django.utils.text import slugify 
from django.urls import reverse 

User = get_user_model() 

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category/', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name'] 
        
    def  __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug':self.slug})
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    sku = models.CharField(max_length=50, unique=True) 
    track_quantity = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    is_active = models.BooleanField(default=True) 
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name    
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) 
        
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug':self.slug})
    
    # def get_primary_image(self):
    #     return self.image.filter(is_primary=True).first()
    
    def get_primary_image(self):
        return self.images.filter(is_primary=True).first()  # Fixed: self.image -> self.images
    
    def get_discount_percentage(self):
        if self.compare_price:
            return int(((self.compare_price - self.price)/ self.compare_price) * 100)
        return 0 
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200,blank=True) 
    #is_primary = models.BooleanField(default=0)
    is_primary = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.IntegerField(default=0)
    class Meta: 
        ordering = ['sort_order']
        
    def __str__(self):
        return f"{self.product.name} = Image {self.id}"
    
class ProductVarient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variants')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    price_adjustment = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'name', 'value'] 

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    title = models.CharField(max_length= 200, blank=True)
    content = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False) 
    # cerated_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)  # Fixed: cerated_at -> created_at
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.rating} stars"

