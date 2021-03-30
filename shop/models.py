from django.db import models
from cms_admin.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    price = models.IntegerField(verbose_name='Price')

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(verbose_name='Status', default=False)

    def __str__(self):
        return self.product.name
