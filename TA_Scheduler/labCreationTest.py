from django.test import TestCase
from django.test import Client
from .models import myLab
from .createCourseFunctions import createLabFunctions
# Create your tests here.

class TestCase_good_createLab(TestCase):
    def setUp(self):
        self.client = Client()

    def test_acceptance_good_createLab(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "COMPSCI"})
        lab_list = response.context["lab_list"]
        labPair = lab_list[0]
        self.assertEqual("1", str(labPair[0]),"Creating a new lab COMPSCI with number 1 failed. Expected lab numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(labPair[1]),"Creating a new lab COMPSCI with number 1 failed. Expected lab names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],"Creating a new lab COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")

    def test_unit_good_createLab(self):
        errorMessage = createLabFunctions.createLab("1", "COMPSCI")
        self.assertEqual("", errorMessage,"Creating a new lab COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")

class TestCase_duplicate_createLab(TestCase):
    def setUp(self):
        self.client = Client()
        self.compsciLab = myLab.objects.create(labNumber="1", labName="COMPSCI")

    def test_acceptance_duplicate_createLab(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "COMPSCI"})
        self.assertEqual("Lab Number Already Exists", response.context["errorMessage"],"Creating a duplicate lab COMPSCI with number 1. Expected errorMessage = 'Lab Number Already Exists'")

    def test_unit_duplicate_createCourse(self):
        errorMessage = createLabFunctions.createLab("1", "COMPSCI")
        self.assertEqual("Lab Number Already Exists", errorMessage,"Creating a duplicate lab COMPSCI with number 1. Expected errorMessage = 'Lab Number Already Exists'")


class TestCase_badInput_createLab(TestCase):
        def setUp(self):
            self.client = Client()

        def test_acceptance_badInput_createLab(self):
            response = self.client.post("/create-lab/", {"courseNumber": "asdf", "labName": "COMPSCI"})
            self.assertEqual("Lab Number Isn't Numeric", response.context["errorMessage"],
                             "Creating a bad input lab COMPSCI with number asdf. Expected errorMessage = 'Lab Number Isn't Numeric'")

        def test_unit_badInput_createLab(self):
            errorMessage = createLabFunctions.createLab("asdf", "COMPSCI")
            self.assertEqual("Lab Number Isn't Numeric", errorMessage,"Creating a bad input lab COMPSCI with number asdf. Expected errorMessage = 'Lab Number Isn't Numeric'")

