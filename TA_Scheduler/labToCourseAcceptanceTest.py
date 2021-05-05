from django.test import TestCase
from django.test import Client
from .models import myLab
from .models import myCourse
import sys
from .assignLabToCourse import labToCourse

class labToCourse_acceptance_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName= "TA")
        self.course = myCourse.objects.create(courseName="MATH", courseNumber= 1,instructorUsername= "admin")

    def test_good_assign(self):
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": self.lab.labNumber,
                                                         "CourseNumber": self.course.courseNumber})
        self.assertEquals(resp.context["message"], "Lab Assigned", "assigning lab to course failed."
                                                                   "Expected <Lab Assigned> message")

    def test_empty_arguments(self):
        #empty labNumber
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": "", "course Number": self.course.courseNumber})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Lab Number Not Provided!>")
        # empty courseNumber
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": self.lab.labNumber, "course Number":""})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Lab Number Not Provided!>")
        # empty labNumber and courseNumber
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": "", "course Number": ""})
        self.assertEquals(resp.context["message"], "No input Provided!",
                          "Assigning lab to course failed. Expected the message <No input Provided!>")

    def test_long_arguments(self):
        #too long lab number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": "7410", "course Number":self.course.courseNumber})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Lab Number Not Provided!>")
        # too long course number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": self.lab.labNumber,"course Number": "7410"})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")
        # too long lab number and too long course number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": "7410", "course Number": "7410"})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")

    def test_max_numbers(self):
        # max integer lab number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Lab Number": sys.maxsize, "course Number": self.course.courseNumber})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Lab Number Not Provided!>")
        # max integer course number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": self.lab.labNumber, "course Number":sys.maxsize})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")
        # max integer lab number and max integer course number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": sys.maxsize, "course Number": sys.maxsize})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")
        # min integer lab number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Lab Number": -sys.maxsize+1, "course Number": self.course.courseNumber})
        self.assertEquals(resp.context["message"], "Lab Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Lab Number Not Provided!>")
        # min integer course number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Lab Number": self.lab.labNumber, "course Number": -sys.maxsize+1})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")
        # min integer lab number and min integer course number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": -sys.maxsize+1, "course Number": -sys.maxsize+1})
        self.assertEquals(resp.context["message"], "Course Number Not Provided!",
                          "Assigning lab to course failed. Expected the message <Course Number Not Provided!>")

    def test_nonexisting_inputs(self):
        # correct but non existing lab number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Lab Number": "999", "course Number": self.course.courseNumber})
        self.assertEquals(resp.context["message"], "This Lab Doesn't Exist!",
                          "Assigning lab to course failed. Expected the message <This Lab Doesn't Exist!>")
        # correct but non existing course number
        resp = self.client.post("/assign-LabToCourse/",
                                {"Lab Number": self.lab.labNumber, "course Number": "999"})
        self.assertEquals(resp.context["message"], "This Course Doesn't Exist!",
                          "Assigning lab to course failed. Expected the message <This Course Doesn't Exist!!>")
        # non existing course and lab number
        resp = self.client.post("/assign-LabToCourse/", {"Lab Number": "999", "course Number": "999"})
        self.assertEquals(resp.context["message"], "This Lab Doesn't Exist!",
                          "Assigning lab to course failed. Expected the message <This Lab Doesn't Exist!>")
