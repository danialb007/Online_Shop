from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Products(models.Model):
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.IntegerField()
    featured = models.BooleanField(default=False)
    discription = models.TextField(max_length=500, default='No description')

class Users(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=80)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    logged_in = models.BooleanField(default=False)
    address = models.TextField(max_length=300)
    phone_number = models.CharField(max_length=16, default='')

class Ips(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default='')
    ip = models.GenericIPAddressField()

class ShoppingList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default='')
    product = models.ManyToManyField(Products)

class Reviews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.CharField(max_length=300)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])