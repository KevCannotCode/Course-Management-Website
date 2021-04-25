from django.test import TestCase, Client
from .models import myAccount
from .createAccount import createAccountFunctions

# Create your tests here.
class CreateNewAccount(TestCase):

    myClient = None
    thingList = None

    def setUp(self):
        self.myClient = Client()
        self.thingList = {'flynnk': 'flynnPassword', 'smithj': 'smithPassword', 'petersont': "petersonPassword"}

        for i in self.thingList.keys():
            temp = myAccount(userName=i, password= self.thingList.get(i))
            temp.save()

    def test_acceptanceTest_newAccount(self):
        resp = self.myClient.post("/create-account/", {"userName": "petersont", "password" : "petersonaPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "account created", "new account not created, user:todd, pass:toddPassword")

    def test_acceptanceTest_UsernameUsed(self):
        for i in self.thingList.keys():
            resp = self.myClient.post("/create-account/", {"name": i, "password": self.thingList.get(i)}, follow=True)
            self.assertEqual(resp.context["message"], "duplicate user", "not stopped from creating duplicate account")

    def test_acceptanceTest_invalidAccountInput(self):
        resp = self.myClient.post("/create-account/", {"name": "", "password": "randomPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "invalid input", "system allowed an invalid input for account creation")

    def test_unitTest_newAccount(self):
        errorMessage = createAccountFunctions.createAccount("williamsg", "williamsPassword")
        self.assertEqual("", errorMessage, "Failed to create account with valid inputs, username: williamsg password: williamsPassword")

    def test_unitTest_duplicateAccount(self):
        errorMessage = createAccountFunctions.createAccount("flynnk", "randomPassword")
        self.assertEqual("Username Already Exists!", errorMessage, "createAccount failed to produce error when trying to create a duplicate account, username: flynnk password: randomPassword")

    def test_unitTest_invalidAccountInput(self):
        errorMessage = createAccountFunctions.createAccount("", "randomPassword")
        self.assertEqual("No Username Provided!", errorMessage, "createAccount failed to produce error message with invalid inputs, username:  password: randomPassword")