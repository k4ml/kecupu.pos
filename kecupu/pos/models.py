from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __unicode__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    customer = models.ForeignKey(Customer)
    items = models.ManyToManyField(Item, through='OrderItem')
    total = models.FloatField()
    store = models.ForeignKey(Store)

class OrderItem(models.Model):
    item = models.ForeignKey(Item)
    order = models.ForeignKey(Order)
    qty = models.IntegerField()
