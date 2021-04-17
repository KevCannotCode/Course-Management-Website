from django.db import models

# Create your models here.

class myAccount(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    userType = models.CharField(max_length=20)
    password = models.CharField(max_length=40)

