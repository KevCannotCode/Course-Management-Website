from django.test import TestCase
from django.test import Client
from setuptools.command.install import install

from .models import myLab
from .models import myLabTA
from .models import myAccount
from .models import myCourse
from .models import myCourseInstructor
from .assignLabToCourse import labToCourse

class AssignLabTAAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName= "kevin")
        self.ta = myAccount.objects.create(userName="kevin", password= "pass", userType= "TA")
        self.instructor = myAccount.objects.create(userName="Inst", password= "pass", userType= "Instructor")
        self.course = myCourse.objects.create(courseName= "MATH", courseNumber= "1",
                                              instructorUserName= self.instructor.userName)
        #assign the course to the instructor
        myCourseInstructor.objects.create(courseNumber= self.course.courseNumber,
                                          instructorUserName= self.instructor.userName)
        #assign the course to the lab
        labToCourse.objects.create(labNumber= self.lab.labNumber, courseNumber= self.course.courseNumber)
        #login
        self.myClient.post("/", {"userName": self.instructor.userName, "password": self.instructor.password})

    def test_good_assign(self):
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
            "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "", "assigning TA to Lab failed."
                                                                 "Expected <> message")
    def test_TA_with_multiple_labs(self):
        # create a new lab and assign it to this course
        newLab = myLab.objects.create(labName="Algebra", labNumber="5", taUserName=self.ta.userName)
        labToCourse.objects.create(labNumber=newLab.labNumber, courseNumber=self.course.courseNumber)
        # test assignment
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
        myLabTA.objects.create(labNumber=self.lab.labNumber, taUserName=self.ta.userName)
        # create a duplicate
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
                                                         "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "This Lab Already Has A TA!", "assigning TA to Lab failed."
                                                       "Expected <This Lab Already Has A TA!> message")

    def test_already_assign(self):
        #assign 2 different TAs to the same lab
        myLabTA.objects.create(labNumber=self.lab.labNumber, taUserName=self.ta.userName)
        #test assignment
        newTA = myAccount.objects.create(userName= "new", password= "0000", userType= "TA")
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.newTA.userName,
                                                         "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "This Lab Already Has A TA!", "assigning TA to Lab failed."
                                                                    "Expected <This Lab Already Has A TA!> message")

    def test_admin_privileges(self):
        adminClient = Client()
        admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        adminClient.post("/", {"userName": admin.userName, "password": admin.password})
        resp = self.adminClient.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
                                                         "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "", "assigning TA to Lab with admin failed. Expected <""> message")

    def test_instructor_without_course(self):
        #create an instructor without a course
        instructor = myAccount.objects.create(userName="impostor", password="pass", userType="Instructor")
        #login
        instructorClient = Client()
        instructorClient = instructorClient.post("/", {"userName": instructor.userName,
                                                       "password": instructor.password})
        #test assignment
        resp = self.client.post("/assign-lab-ta.html/", {"Username": self.ta.userName,
                                                         "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "This Instructor Doesn't Have A Course!", "assigning TA to Lab "
                "with admin failed. Expected <This Instructor Doesn't Have A Course!> message")

    def test_unauthorized_assignment(self):
        #create an unauthorized instructor
        impostor = myAccount.objects.create(userName="impostor", password="pass", userType="Instructor")
        #assign this instructor to another course
        course = myCourse.objects.create(courseName="Test", courseNumber="123",
                                         instructorUserName=impostor.userName)
        myCourseInstructor.objects.create(courseNumber=course.courseNumber,
                                          instructorUserName=impostor.userName)
        #login
        impostorClient = Client()
        impostorClient = impostorClient.post("/", {"userName": impostor.userName, "password": impostor.password})
        #test the assignment
        resp = impostorClient.post("/assign-lab-ta.html/",
                                   {"Username": self.ta.userName, "Lab Number": self.lab.labNumber})
        self.assertEquals(resp.context["message"], "Unauthorized Assignment!", "assigning TA to Lab "
        "with admin failed. Expected <Unauthorized Assignment!> message")
