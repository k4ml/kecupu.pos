from django.db import models
from django.contrib.auth.models import User

#from kecupu.pos.exceptions import NullTotalException

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
    price = models.DecimalField(max_digits=7, decimal_places=2)
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    customer = models.ForeignKey(Customer)
    items = models.ManyToManyField(Item, through='OrderItem')
    total = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    store = models.ForeignKey(Store)

    def save(self, *args, **kwargs):
        if len(self.orderitem_set.all()) == 0:
            self.total = 0
        else:
            self.total = reduce((lambda x,y: x+y), [orderitem.total for orderitem in self.orderitem_set.all()])
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    item = models.ForeignKey(Item)
    order = models.ForeignKey(Order)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.price * int(self.qty)
        super(OrderItem, self).save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    method = models.CharField(max_length=50)
    checque_no = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
