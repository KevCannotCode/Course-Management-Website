from django.test import TestCase
from django.test import Client
from .models import myCourse
from .models import myAccount
from .createCourseFunctions import createCourseFunctions
# Create your tests here.


class TestCase_empty_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "", "courseName": ""})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Number or Course Name Provided!", response.context["errorMessage"],"Creating a new course with empty fields. Expected errorMessage = 'No Course Number or Course Name Provided!'")

    def test_unit_emptycreateCourse(self):
        errorMessage = createCourseFunctions.createCourse("", "")
        self.assertEqual("No Course Number or Course Name Provided!", errorMessage,"Creating a new course with empty fields. Expected errorMessage = 'No Course Number or Course Name Provided!'")

class TestCase_empty_courseNumber_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_courseNumber_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "", "courseName": "COMPSCI"})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Number Provided!", response.context["errorMessage"],"Creating a new course COMPSCI with number empty. Expected errorMessage = 'No Course Number Provided!'")

    def test_unit_empty_courseNumber_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("", "COMPSCI")
        self.assertEqual("No Course Number Provided!", errorMessage,"Creating a new course COMPSCI with number empty. Expected errorMessage = 'No Course Number Provided!'")

class TestCase_empty_courseName_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_courseName_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": ""})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Name Provided!", response.context["errorMessage"],"Creating a new empty course with number 1. Expected errorMessage = 'No Course Name Provided!'")

    def test_unit_empty_courseName_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "")
        self.assertEqual("No Course Name Provided!", errorMessage,"Creating a new empty course with number 1. Expected errorMessage = 'No Course Name Provided!'")

class TestCase_good_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_good_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        course_list = response.context["course_list"]
        coursePair = course_list[0]
        self.assertEqual("1", str(coursePair[0]),"Creating a new course COMPSCI with number 1 failed. Expected course numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(coursePair[1]),"Creating a new course COMPSCI with number 1 failed. Expected course names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],"Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")

    def test_unit_good_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCI")
        self.assertEqual("", errorMessage,"Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")


class TestCase_duplicate_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})
        self.compsciCourse = myCourse.objects.create(courseNumber="1", courseName="COMPSCI")

    def test_acceptance_duplicate_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        self.assertEqual("Course Number Already Exists!", response.context["errorMessage"],"Creating a duplicate course COMPSCI with number 1. Expected errorMessage = 'Course Number Already Exists'")

    def test_unit_duplicate_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCI")
        self.assertEqual("Course Number Already Exists!", errorMessage,"Creating a duplicate course COMPSCI with number 1. Expected errorMessage = 'Course Number Already Exists'")


class TestCase_badInput_courseNumber_notNumeric_createCourse(TestCase):
        def setUp(self):
            self.client = Client()
            self.admin = myAccount.objects.create(userName="admin", password="password")
            self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

        def test_acceptance_badInput_courseNumber_notNumeric_createCourse(self):
            response = self.client.post("/create-course/", {"courseNumber": "asdf", "courseName": "COMPSCI"})
            self.assertEqual("Course Number Isn't Numeric!", response.context["errorMessage"],
                             "Creating a bad input course COMPSCI with number asdf. Expected errorMessage = 'Course Number Isn't Numeric'")

        def test_unit_badInput_courseNumber_notNumeric_createCourse(self):
            errorMessage = createCourseFunctions.createCourse("asdf", "COMPSCI")
            self.assertEqual("Course Number Isn't Numeric!", errorMessage,"Creating a bad input course COMPSCI with number asdf. Expected errorMessage = 'Course Number Isn't Numeric'")


class TestCase_badInput_courseNumber_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_badInput_courseNumber_tooLong_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "99999999999", "courseName": "COMPSCI"})
        self.assertEqual("Course Number Is Too Long!", response.context["errorMessage"],
                         "Creating a bad input too long course COMPSCI with number 99999999999. Expected errorMessage = 'Course Number Is Too Long!'")

    def test_unit_badInput_courseNumber_tooLong_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("99999999999", "COMPSCI")
        self.assertEqual("Course Number Is Too Long!", errorMessage,
                         "Creating a bad input too long course COMPSCI with number 99999999999. Expected errorMessage = 'Course Number Is Too Long!'")


class TestCase_badInput_courseName_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_badInput_courseName_tooLong_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI"})
        self.assertEqual("Course Name Is Too Long!", response.context["errorMessage"],
                         "Creating a bad input too long course COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI with number 1. Expected errorMessage = 'Course Name Is Too Long!'")

    def test_unit_badInput_courseName_tooLong_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI")
        self.assertEqual("Course Name Is Too Long!", errorMessage,
                         "Creating a bad input too long course COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI with number 1. Expected errorMessage = 'Course Name Is Too Long!'")

