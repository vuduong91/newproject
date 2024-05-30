from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Category(models.Model):
    nameCate = models.CharField(max_length=255)
    def __str__(self):
        return self.nameCate
class Product(models.Model):
    nameProduct = models.CharField(max_length=255)
    nameCate=models.ForeignKey(Category, on_delete=models.CASCADE)
    decripsion = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    cost = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/')
    maxspeed = models.CharField(max_length=255)
    maxtouque = models.CharField(max_length=255)
    def __str__(self):
        return self.nameProduct
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True)
    dateorder = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user) if self.user else ''

class OrderDetail(models.Model):
    cost = models.IntegerField(default=11)
    quanity = models.IntegerField(default=11)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True)
    def total(self):
        return OrderDetail.cost * OrderDetail.quanity
    def __str__(self):
        return str(self.product) if self.product else ''

User.orderdetail = property(lambda u: OrderDetail.objects.get_or_create(user=u)[0])