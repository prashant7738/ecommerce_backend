from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.product_name
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) # True when payment is confirmed
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    

# --- Order Item Model ---
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # Product ID
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # Order ID
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'