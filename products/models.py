from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Order(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    STATE_CHOICES = (
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    status = models.CharField(max_length=20,choices=STATE_CHOICES, default='Pending')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10,
                                       decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name








class Product(models.Model):
    
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/',null=True,blank=True)
    stock = models.IntegerField()
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    order = models.ForeignKey(Order,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user','products')
# class Product(models.Model):

#     name = models.CharField(max_length=100)
#     price = models.IntegerField()
#     description = models.TextField()

class Whishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
            
               fields = ['user','products'],
               name = 'unique_user_product'

            )
        ]
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user', 'products'],
    #             name='unique_user_product'
    #         )
    #     ]