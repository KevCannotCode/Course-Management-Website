from django.test import TestCase
from django.test import Client
from .models import myAccount
from TA_Scheduler.Login import Login
from .createCourseFunctions import createCourseFunctions
# Create your tests here.

class loginUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.adminUser = myAccount.objects.create(name="admin", password="password")
        self.standardUser = myAccount.objects.create(name="dude", password="pass")
        self.emptyUser = myAccount.objects.create(name="", password="")

    def good_login_test(self):
        #the admin and standard username should be found in the database
        self.assertEquals(True,Login(self.adminUser.userName, self.adminUser.password), "The username exists but was not found")
        self.assertEquals(True, Login(self.standardUser.userName, self.standardUser.password), "The username exists but was not found")

    def wrong_username_test(self):
        self.assertEquals(False, Login("wrong", self.adminUser.password), "The username was wrong but login returned true")
        self.assertEquals(False, Login("wrong", self.standardUser.password), "The username was wrong but login returned true")

    def wrong_password_test(self):
        self.assertEquals(False, Login(self.standardUser.userName, "wrong" ), "The password was wrong but login returned true")
        self.assertEquals(False, Login(self.adminUser.userName, "wrong" ), "The password was wrong but login returned true")


    def empty_inputs_test(self):
        #empty username
        self.assertEquals(False, Login(self.emptyUser.userName, self.emptyUser.password), "The username was empty but login returned true")
        #empty password
        self.assertEquals(False, Login(self.standardUser.userName, self.standardUser.password), "The password was empty but login returned true")
        #both inputs empty
        self.assertEquals(False, Login(self.emptydUser.userName, self.emptyUser.password), "Both inputs were empty but login returned true")

    def input_mismatch_test(self):
        self.assertEquals(False, Login(self.adminUser.userName, self.standardUser.password),"The inputs don't match but login returned true")
