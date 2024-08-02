from django.db import models
from shop.models import *
from account.models import *


# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ('C0', 'Confirm'),
        ('Q1', 'In the review queue'),
        ('R2', 'Received from the seller'),
        ('P3', 'Preparing the order'),
        ('D4', 'Delivery to the post office'),
        ('D5', 'Delivery to the customer'),
        ('R6', 'Return of the cost due to lack of stock'),
        ('N7', 'Not Paid')
    ]

    buyer = models.ForeignKey(ShopUser, on_delete=models.SET_NULL, related_name='orders', null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status_order = models.CharField(max_length=2, choices=STATUS_CHOICES, default='In the review queue')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 1000:
            return 20000
        elif 1000 <= weight <= 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        price = self.get_post_cost() + self.get_total_cost()
        return price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.quantity * self.weight


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
