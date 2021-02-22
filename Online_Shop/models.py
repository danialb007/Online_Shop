from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.IntegerField()
    featured = models.BooleanField(default=False)
    discription = models.TextField(max_length=500, default='No description')

class Users(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    logged_in = models.BooleanField(default=False)
    address = models.TextField(max_length=200)

class Ips(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default='')
    ip = models.GenericIPAddressField()

class ShoppingList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default='')
    product = models.ManyToManyField(Products)