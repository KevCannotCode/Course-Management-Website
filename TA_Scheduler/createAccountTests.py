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

    def acceptanceTest_newAccount(self):
        resp = self.myClient.post("/create-account/", {"userName": "petersont", "password" : "petersonaPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "account created", "new account not created, user:todd, pass:toddPassword")

    def acceptanceTest_UsernameUsed(self):
        for i in self.thingList.keys():
            resp = self.myClient.post("/create-account/", {"name": i, "password": self.thingList.get(i)}, follow=True)
            self.assertEqual(resp.context["message"], "duplicate user", "not stopped from creating duplicate account")

    def acceptanceTest_invalidAccountInput(self):
        resp = self.myClient.post("/create-account/", {"name": "", "password": "randomPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "invalid input", "system allowed an invalid input for account creation")

    def unitTest_newAccount(self):
        errorMessage = createAccountFunctions.createAccount("williamsg", "williamsPassword")
        self.assertEqual("", errorMessage, "Failed to create account with valid inputs, username: williamsg password: williamsPassword")

    def unitTest_duplicateAccount(self):
        errorMessage = createAccountFunctions.createAccount("flynnk", "randomPassword")
        self.assertEqual("An account with this username already exits", errorMessage, "createAccount failed to produce error when trying to create a duplicate account, username: flynnk password: randomPassword")

    def unitTest_invalidAccountInput(selfself):
        errorMessage = createAccountFunctions.createAccount("", "randomPassword")
        self.assertEqual("Invalid username and/or password", errorMessage, "createAccount failed to produce error message with invalid inputs, username:  password: randomPassword")