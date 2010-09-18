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
