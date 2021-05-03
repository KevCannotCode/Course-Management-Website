from django.test import TestCase
from django.test import Client
from .models import myAccount
from TA_Scheduler.myLogin import myLogin
from .createCourseFunctions import createCourseFunctions
# Create your tests here.

class loginUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.adminUser = myAccount.objects.create(userName="admin", password="password")
        self.standardUser = myAccount.objects.create(userName="dude", password="pass")
        self.emptyUser = myAccount.objects.create(userName="", password="")
        self.longUsername = "0123456789012345678901234567890123456789blablabla"
        self.longPassword = "0123456789012345678901234567890123456789blablabla"
    def test_good_login(self):
        #the admin and standard username should be found in the database
        self.assertEquals(myLogin.login(self.adminUser.userName, self.adminUser.password), "", "The credentials were correct but the login failed")
        self.assertEquals(myLogin.login(self.standardUser.userName, self.standardUser.password), "", "The credentials were correct but the login failed")

    def test_long_inputs(self):
        #long username
        self.assertEquals(myLogin.login(self.longUsername, self.adminUser.password), "The Username Is Too Long!",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login(self.longUsername, self.standardUser.password), "The Username Is Too Long!", "The username was wrong but login did not fail")
        #long password
        self.assertEquals(myLogin.login(self.adminUser.userName, self.longPassword), "The Password Is Too Long!",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login(self.standardUser.userName, self.longPassword),"The Password Is Too Long!", "The username was wrong but login did not fail")
        #both inputs are too long
        self.assertEquals(myLogin.login(self.longUsername, self.longPassword),"The Username Is Too Long!",  "The username was wrong but login did not fail")

    def test_wrong_username(self):
        self.assertEquals(myLogin.login("wrong", self.adminUser.password), "User Doesn't Exist",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login("wrong", self.standardUser.password),"User Doesn't Exist" , "The username was wrong but login did not fail")

    def test_wrong_password(self):
        self.assertEquals(myLogin.login(self.standardUser.userName, "wrong" ),"Incorrect Password!" , "The password was wrong but login worked")
        self.assertEquals(myLogin.login(self.adminUser.userName, "wrong" ), "Incorrect Password!","The password was wrong but login worked")


    def test_empty_inputs(self):
        #empty username
        self.assertEquals("No Username Provided!", myLogin.login(self.emptyUser.userName, self.emptyUser.password),"The username was empty but login worked")
        #empty password
        self.assertEquals("No Password Provided!", myLogin.login(self.standardUser.userName, self.emptyUser.password), "The password was empty but  worked")
        #both inputs empty
        self.assertEquals("No Username Provided!", myLogin.login(self.emptyUser.userName, self.emptyUser.password), "Both inputs were empty but login worked")

    def test_input_mismatch(self):
        self.assertEquals("Incorrect Password!", myLogin.login(self.adminUser.userName, self.standardUser.password),"The inputs don't match but login worked")
