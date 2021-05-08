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
        self.taDup = myAccount.objects.create(userName="kevin2", password="pass2", userType="TA")
        self.labDup = myLab.objects.create(labName="Algebra", labNumber="5", taUserName=self.taDup.userName)
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName=self.ta.userName)
        self.assignDuplicate = myLabTA.objects.create(labNumber=self.labDup.labNumber, taUserName=self.taDup.userName)

    def test_good_assign(self):
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
            "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "", "assigning TA to Lab failed."
                                                                 "Expected <> message")
        #assigning the same TA to a different lab
        newLab = myLab.objects.create(labName="Algebra", labNumber="5", taUserName=self.ta.userName)
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
                                                         "Lab Number": newLab.labNumber})
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

    def test_non_existing_inputs(self):
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

    def test_duplicate_assign(self):

        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.taDup.userName,
                                                         "Lab Number": self.labDup.labNumber})
        self.assertEquals(resp.context["message"], "This Lab Already Has A TA!", "assigning TA to Lab failed."
                                                       "Expected <This Lab Already Has A TA!> message")

    def test_already_assign(self):
        #assign 2 different TAs to the same lab
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
                                                         "Lab Number": self.labDup.labNumber})
        self.assertEquals(resp.context["message"], "This Lab Already Has A TA!", "assigning TA to Lab failed."
                                                                                 "Expected <This Lab Already Has A TA!> message")