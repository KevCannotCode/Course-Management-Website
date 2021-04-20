from django.test import TestCase
from django.test import Client
from .models import myAccount
from .models import myCourse
from .models import myCourseInstructors
# Create your tests here.



class TestCase_good_createCourse(TestCase):
    def setUp(self):
        self.client = Client()

    def test_good_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        course_list = response.context["course_list"]
        coursePair = course_list[0]
        self.assertEqual("1", str(coursePair[0]),"Creating a new course COMPSCI with number 1 failed. Expected course numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(coursePair[1]),"Creating a new course COMPSCI with number 1 failed. Expected course names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],"Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")


class TestCase_duplicate_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.compsciCourse = myCourse.objects.create(courseNumber="1", courseName="COMPSCI")

    def test_good_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        self.assertEqual("Course Number Already Exists", response.context["errorMessage"],"Creating a duplicate course COMPSCI with number 1. Expected errorMessage = 'Course Number Already Exists'")


class TestCase_badInput_createCourse(TestCase):
        def setUp(self):
            self.client = Client()

        def test_good_createCourse(self):
            response = self.client.post("/create-course/", {"courseNumber": "asdf", "courseName": "COMPSCI"})
            self.assertEqual("Course Number Isn't Numeric", response.context["errorMessage"],
                             "Creating a bad input course COMPSCI with number asdf. Expected errorMessage = 'Course Number Isn't Numeric'")