from django.test import TestCase
from django.test import Client
from .models import myAccount
from .createLabFunctions import createLabFunctions


# Create your tests here.

class testCreateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_createSection(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section 1"})
        lab_list = response.context["lab_list"]
        testLab = lab_list[0]
        self.assertEqual("1", str(testLab[0]), "New section creation failed at sectionNumber")
        self.assertEqual("Section 1", str(testLab[1]), "New section creation failed at sectionName")
        self.assertEqual("", response.context["errorMessage"],
                         "Error creating new section")

    def test_unit_createSection(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.assertEqual("", errorMessage, "Error creating new section")


class testDuplicateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.newLab = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_duplicateSection(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section 1"})
        self.assertEqual("Lab Number Already Exists!", response.context["errorMessage"],
                         "Error creating new section, labNumber already exists")

    def test_unit_duplicateSection(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.assertEqual("Lab Number Already Exists!", errorMessage,
                         "Error creating new section, labNumber already exists")


class testSectionInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_labNumberNumeric(self):
        response = self.client.post("/create-lab/", {"labNumber": "one", "labName": "Section 1"})
        self.assertEqual("Lab Number Isn't Numeric!", response.context["errorMessage"],
                         "Error creating new section, labNumber is not a number")

    def test_unit_labNumberNumeric(self):
        errorMessage = createLabFunctions.createLab(labNumber="one", labName="Section 1")
        self.assertEqual("Lab Number Isn't Numeric!", errorMessage,
                         "Error creating new section, labNumber is not a number")

    def test_acceptance_labNumberTooLong(self):
        response = self.client.post("/create-lab/", {"labNumber": "11111111111", "labName": "Section 1"})
        self.assertEqual("Lab Number Is Too Long!", response.context["errorMessage"],
                         "Error creating new section, labNumber is greater than 10 characters")

    def test_unit_labNumberTooLong(self):
        errorMessage = createLabFunctions.createLab(labNumber="11111111111", labName="Section 1")
        self.assertEqual("Lab Number Is Too Long!", errorMessage,
                         "Error creating new section, labNumber is greater than 10 characters")

    def test_acceptance_labNameTooLong(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section1Section1Section1"})
        self.assertEqual("Lab Name Is Too Long!", response.context["errorMessage"],
                         "Error creating new section, labName is greater than 20 characters")

    def test_unit_labNameTooLong(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section1Section1Section1")
        self.assertEqual("Lab Name Is Too Long!", errorMessage,
                         "Error creating new section, labName is greater than 20 characters")


class testSectionEmptyInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_labNumberEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "", "labName": "Section 1"})
        self.assertEqual("No Lab Number Provided!", response.context["errorMessage"],
                         "Error creating new section, labNumber is empty")

    def test_unit_labNumberEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="", labName="Section 1")
        self.assertEqual("No Lab Number Provided!", errorMessage,
                         "Error creating new section, labNumber is empty")

    def test_acceptance_labNameEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": ""})
        self.assertEqual("No Lab Name Provided!", response.context["errorMessage"],
                         "Error creating new section, labName is empty")

    def test_unit_labNameEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="")
        self.assertEqual("No Lab Name Provided!", errorMessage,
                         "Error creating new section, labName is empty")

    def test_acceptance_bothEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "", "labName": ""})
        self.assertEqual("No Lab Number or Lab Name Provided!", response.context["errorMessage"],
                         "Error creating new section, both labNumber and labName are empty")

    def test_unit_bothEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="", labName="")
        self.assertEqual("No Lab Number or Lab Name Provided!", errorMessage,
                         "Error creating new section, both labNumber and labName are empty")
