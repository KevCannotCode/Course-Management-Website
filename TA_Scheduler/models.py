from django.db import models

# Create your models here.

class myAccount(models.Model):
    userName = models.CharField(max_length=40)
    password = models.CharField(max_length=40)

class myCourse(models.Model):
    courseName = models.CharField(max_length=20)
    courseNumber = models.IntegerField()

class myLab(models.Model):
    labName = models.CharField(max_length=20)
    labNumber = models.IntegerField()

class myContact(models.Model):
    userName = models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=20)
    emailAddress = models.CharField(max_length=40)

class myCourseInstructors(models.Model):
    courseNumber = models.IntegerField()
    userName = models.CharField(max_length=40)
