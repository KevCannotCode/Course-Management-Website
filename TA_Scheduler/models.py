from django.db import models

# Create your models here.

class myAccount(models.Model):
    userName = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    userType = models.CharField(max_length=40)

class myCourse(models.Model):
    courseName = models.CharField(max_length=20)
    courseNumber = models.IntegerField()
    instructorUserName = models.CharField(max_length=40)


class myLab(models.Model):
    labName = models.CharField(max_length=20)
    labNumber = models.IntegerField()
    taUserName = models.CharField(max_length=40)

class myContact(models.Model):
    userName = models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=20)
    emailAddress = models.CharField(max_length=40)

class myCourseInstructor(models.Model):
    courseNumber = models.IntegerField()
    instructorUserName = models.CharField(max_length=40)


class myLabTA(models.Model):
    labNumber = models.IntegerField()
    taUserName = models.CharField(max_length=40)
    labCount = models.IntegerField()

class labToCourse(models.Model):
    labNumber = models.IntegerField()
    courseNumber = models.IntegerField()
