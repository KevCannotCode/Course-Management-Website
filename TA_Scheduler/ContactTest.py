from django.test import TestCase
from django.test import Client
from .models import myContact
from TA_Scheduler.Contact import Contact
# Create your tests here.

# Create your tests here.
class login_test(TestCase):
    def setUp(self):
        # Setup client, account and number and email
        self.client = Client()
        self.adminUser = myContact.objects.create(number="4146968888", email="admin@uwm.edu")
        self.standardUser = myContact.objects.create(number="4147774444", email="user@uwm.edu")
        self.emptyUser = myContact.objects.create(number="", email="")

    def test_good_form(self):
        # Good input with admin
        response = self.client.post("/account/edit",
                                         {"Number": self.adminUser.number, "email": self.adminUser.email})
        self.assertEqual("Please enter a password and a username", response.context["message"],
                         "Contact information updated: phone: 414-696-8888, email: admin@uwm.edu")
        # contact with empty phone number and email
        response = self.client.post("/account/edit",
                                    {"Number": self.standardUser.number, "email": self.standardUser.email})
        self.assertEqual("Please enter a password and a username", response.context["message"],
                            "Contact information updated: phone: 414-777-4444, email: user@uwm.edu")

    def test_empty_form(self):
        # contact with empty phone number
        response = self.client.post("/account/edit",
                                            {"Number": self.emptyUser.number, "email": self.standardUser.email})
        self.assertEqual("Please enter contact information", response.context["message"],
                      "Phone number and Email are required",
                   "Entering phone number is required to update account ")
        # contact with empty email
        response = self.client.post("/account/edit",
                                    {"Number": self.standardUser.number, "email": self.emptyUser.email})
        self.assertEqual("Please enter contact information", response.context["message"],
                      "Phone number and Email are required", "Entering email is required to update account ")
        # contact with empty phone number and email

        response = self.client.post("/account/edit",
                                    {"Number": self.emptyUser.number, "email": self.emptyUser.email})
        self.assertEqual("Please enter contact information", response.context["message"],
                "Phone number and Email are required", "Entering contact information is required to update account.")

    def test_BadInput_Contact(self):  # we test existing username and password that do not match
        # Incorrect Email format
        response = self.client.post("/account/edit", {"1412005555": self.standardUser.number,
                "useratuwmedu": self.standardUser.email})
        self.assertEqual("Incorrect email format", response.context["message"],
                "Incorrect Email Format, an example of the correct format is example@website.org.  Expected <Incorrect email> message")
        # Login with a standard password and admin username
        response = self.client.post("/account/edit", {"151561651561666": self.adminUser.number,
                                        "email@uwm.edu": self.standardUser.email})
        self.assertEqual("Incorrect number format", response.context["message"],
        "Incorrect number Format, an example of the correct format is 4140001111.  Expected <Incorrect number> message")

    def duplicate_info_Contact(self):  # testing for contact info already linked to another account
        # Duplicate phone numbers
        response = self.client.post("/account/edit", {"4146968888": self.standardUser.number,
                                            "email@uwm.edu": self.standardUser.email})
        self.assertEqual("Duplicate Phone Number", response.context["message"],
                     "Phone Number already belongs to another account. Check with admin or try another Expected Duplicate number message")
        # Duplicate emails
        response = self.client.post("/account/edit", {"1111111111": self.adminUser.number,
                        "user@uwm.edu": self.standardUser.email})
        self.assertEqual("Duplicate Email", response.context["message"],
           "Email already belongs to another account. Check with admin or try another Expected Duplicate email message")
        # Both duplicate
        response = self.client.post("/account/edit", {"4146968888": self.adminUser.number,
                         "user@uwm.edu": self.standardUser.email})
        self.assertEqual("Both Phone and Email are duplicate", response.context["message"],
        "Both Phone and Email are already connected to another account. Expected Duplicate number and email message")
