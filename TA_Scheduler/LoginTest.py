from django.test import TestCase
from django.test import Client
from .models import MyUser
from .models import Stuff
# Create your tests here.
class login_test(TestCase):
    def setUp(self):
        #Setup client, account and something in the list
        self.client = Client()
        self.adminUser = MyUser.objects.create(name="admin", password="password")
        self.standardUser = MyUser.objects.create(name="dude", password = "pass")
        self.nullsUser = MyUser.objects.create(name= None, password= None )
        self.emptyUser = MyUser.objects.create(name= "", password= "" )
        #create a course

    def test_good_login(self):
        #Good login with standard user
        response = self.client.post("/", {"name": , "password": adminUser})
        #Check redirect
        self.assertEqual("/things/", response.url,"Logging in as admin with correct password admin failed. Expected redirect URL to be /things/")




class TestCase_bad_login(TestCase):
    def setUp(self):
        # Setup client, account and something in the list
        self.client = Client()
        self.adminUser = MyUser.objects.create(name="admin", password="admin")
        self.userThing = Stuff.objects.create(name="something", owner=self.adminUser)

    def test_bad_login(self):
        #Login with bad incorrect password
        response = self.client.post("/", {"name": "admin", "password": "password"})
        #Check message for bad password
        self.assertEqual("bad password", response.context["message"], "Logging in as admin with wrong password password. Expected bad password message")




class TestCase_list(TestCase):
    def setUp(self):
        # Setup client, account and something in the list
        self.client = Client()
        self.adminUser = MyUser.objects.create(name="admin", password="admin")
        self.userThing = Stuff.objects.create(name="something", owner=self.adminUser)

    def test_list(self):
        #Login with adminUser
        response1 = self.client.post("/", {"name": "admin", "password": "admin"})
        #Check redirect
        self.assertEqual("/things/", response1.url)
        response = self.client.post("/things/", {"stuff": "new something"})
        #Save list and length
        listContent = response.context["things"]
        listLen = len(listContent)
        #Check length and value
        print(listContent)
        self.assertEqual(2, listLen)
        self.assertEqual("new something", listContent[listLen-1], "Expected 'new something'. Adding to the list failed!")