from django.test import TestCase
from django.test import Client
from .models import myLab
from .models import myLabTA
from .models import myAccount
import sys
from .assignLabToCourse import labToCourse

class AssignLabTAAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = myAccount.objects.create(userName="kevin", password="pass", userType="TA")
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName=self.ta.userName)
        self.assignDuplicate = myLabTA.objects.create(labNumber=self.lab.labNumber, taUserName=self.ta.userName)

    def test_good_assign(self):
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
            "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "", "assigning TA to Lab failed."
                                                                   "Expected <> message")

    def test_empty_arguments(self):
        #empty labNumber
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName, "Lab Number": ""})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning TA to Lab failed. Expected the message <Lab Number Not Provided!>")
        # empty username
        resp = self.client.post("/assign-lab-ta.html/", {"Username":"", "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "TA Username Not Provided!",
                          "Assigning TA to Lab failed. Expected the message <Lab Number Not Provided!>")
        # empty labNumber and TA username
        resp = self.client.post("/assign-lab-ta.html/", {"Username": "", "Lab Number": ""})
        self.assertEquals(resp.context["message"], "No input Provided!",
                          "Assigning TA to Lab failed. Expected the message <No input Provided!>")

    def test_long_arguments(self):
        #too long lab number
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName, "Lab Number": "7410"})
        self.assertEquals(resp.context["message"], "Invalid Lab Number!",
                          "Assigning TA to Lab failed. Expected the message <Invalid Lab Number!>")
        # too long username (more than 40 characters for username)
        resp = self.client.post("/assign-lab-ta.html/", {"Username": "045780123456789012345678901234567890123456789",
                                                         "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "Invalid TA Username!",
                          "Assigning TA to Lab failed. Expected the message <Invalid TA Username!>")
        # too long lab number and too username
        resp = self.client.post("/assign-lab-ta.html/", {"Username": "045780123456789012345678901234567890123456789",
                                                         "Lab Number": "7410"})
        self.assertEquals(resp.context["message"], "Invalid Lab Number and TA Username!",
                          "Assigning TA to Lab failed. Expected the message <Invalid Lab Number and TA Username!>")

    def test_nonexisting_inputs(self):
        # correct username but non existing lab number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Username": self.ta.userName, "Lab Number": "999"})
        self.assertEquals(resp.context["message"], "Invalid Lab Number!",
                          "Assigning TA to Lab failed. Expected the message <Invalid Lab Number!>")
        # correct lab number but non existing username
        resp = self.client.post("/assign-LabToCourse/",
                                {"Username": "8888sdff", "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "Invalid TA username!",
                          "Assigning TA to Lab failed. Expected the message <Invalid TA username!>")
        # non existing course and lab number
        resp = self.client.post("/assign-LabToCourse/", {"Username": "ffff999", "Lab Number": "999"})
        self.assertEquals(resp.context["message"], "Invalid Lab Number and TA Username!",
                          "Assigning TA to Lab failed. Expected the message <Invalid Lab Number and TA Username!>")
