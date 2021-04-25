from django.test import TestCase
from django.test import Client
from .models import myContact
from TA_Scheduler.Contact import Contact
# Create your tests here.

class TestContact(TestCase):
    def setUp(self):
        self.client = Client()
        self.goodContact = Contact.createContact(4146142209, "good@uwm.edu")
        self.emptyContact = Contact.createContact("", "")

    def create_good_contact(self):
        response = self.client.post("/profile/", {"phoneNumber": "1", "courseName": "COMPSCI"})
        course_list = response.context["course_list"]
        coursePair = course_list[0]
        self.assertEqual("1", str(coursePair[0]),
                         "Creating a new course COMPSCI with number 1 failed. Expected course numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(coursePair[1]),
                         "Creating a new course COMPSCI with number 1 failed. Expected course names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],
                         "Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")