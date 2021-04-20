from django.test import TestCase, Client
from .models import MyUser

# Create your tests here.
class CreateNewAccount(TestCase):

    myClient = None
    thingList = None

    def setUp(self):
        self.myClient = Client()
        self.thingList = {'flynnk': 'flynnPassword', 'smithj': 'smithPassword', 'petersont': "petersonPassword"}

        for i in self.thingList.keys():
            temp = MyUser(name=i, password= self.thingList.get(i))
            temp.save()

    def test_newAccount(self):
        resp = self.myClient.post("/", {"name": "petersont", "password" : "petersonaPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "account created", "new account not created, user:todd, pass:toddPassword")

    def test_UsernameUsed(self):
        for i in self.thingList.keys():
            resp = self.myClient.post("/", {"name": i, "password": self.thingList.get(i)}, follow=True)
            self.assertEqual(resp.context["message"], "duplicate user", "not stopped from creating duplicate account")

