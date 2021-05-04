from django.test import TestCase
from django.test import Client
from .models import myLab
from .models import myCourse
from .labToCourse import labToCourse

class labToCourse_acceptance_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.lab = myLab.objects.create(labName= "MATHLAB", labNumber="202", taUserName= "TA")
        self.course = myCourse.objects.create(courseName= "MATH", courseNumber= 1,instructorUsername= "admin")

    def test_good_assign(self):
        response = self.client.post("/assign-LabToCourse/", {"labNumber"})
    def test_empty_arguments(self):
        self.assertEquals()