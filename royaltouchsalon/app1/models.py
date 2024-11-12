from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey("app1.Product", on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    HOME_SERVICE_CHOICES = [
        ('professional_makeup','Professional Makeup'),
        ('manicure_pedicure','Manicure Pedicure'),
        ('body_treatment','Body Treatment'),
        ('hair_treatment','Hair Treatment'),
    ]
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length = 20, choices = HOME_SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    message = models.TextField(blank = True,null=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_name} - {self.service} on {self.appointment_date} at {self.appointment_time}'
    

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hair' , 'Hair Care'),
        ('skin' , 'Skin Care'),
        ('body' , 'Body Care'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/',blank=True,null=True)
    category= models.CharField(max_length=50,choices=CATEGORY_CHOICES,default='hair')
    available=models.BooleanField(default=True)
    shipping_options = models.TextField(default="Standard shipping")

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

