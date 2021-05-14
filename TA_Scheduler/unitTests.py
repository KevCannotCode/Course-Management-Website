import unittest
import sys
from django.test import TestCase, Client
from .models import myAccount, myCourse, myLab
from TA_Scheduler.myLogin import myLogin
from .createAccount import createAccountFunctions
from .createCourseFunctions import createCourseFunctions
from .createLabFunctions import createLabFunctions
from .assignLabToCourse import assignLabToCourse
from .myCourseInstructor import myCourseInstructor
from .assignLabTA import assignLabTA

class loginUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.adminUser = myAccount.objects.create(userName="admin", password="password")
        self.standardUser = myAccount.objects.create(userName="dude", password="pass")
        self.emptyUser = myAccount.objects.create(userName="", password="")
        self.longUsername = "0123456789012345678901234567890123456789blablabla"
        self.longPassword = "0123456789012345678901234567890123456789blablabla"
    def test_good_login(self):
        #the admin and standard username should be found in the database
        self.assertEquals(myLogin.login(self.adminUser.userName, self.adminUser.password), "", "The credentials were correct but the login failed")
        self.assertEquals(myLogin.login(self.standardUser.userName, self.standardUser.password), "", "The credentials were correct but the login failed")

    def test_long_inputs(self):
        #long username
        self.assertEquals(myLogin.login(self.longUsername, self.adminUser.password), "The Username Is Too Long!",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login(self.longUsername, self.standardUser.password), "The Username Is Too Long!", "The username was wrong but login did not fail")
        #long password
        self.assertEquals(myLogin.login(self.adminUser.userName, self.longPassword), "The Password Is Too Long!",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login(self.standardUser.userName, self.longPassword),"The Password Is Too Long!", "The username was wrong but login did not fail")
        #both inputs are too long
        self.assertEquals(myLogin.login(self.longUsername, self.longPassword),"The Username Is Too Long!",  "The username was wrong but login did not fail")

    def test_wrong_username(self):
        self.assertEquals(myLogin.login("wrong", self.adminUser.password), "User Doesn't Exist",  "The username was wrong but login did not fail")
        self.assertEquals(myLogin.login("wrong", self.standardUser.password),"User Doesn't Exist" , "The username was wrong but login did not fail")

    def test_wrong_password(self):
        self.assertEquals(myLogin.login(self.standardUser.userName, "wrong" ),"Incorrect Password!" , "The password was wrong but login worked")
        self.assertEquals(myLogin.login(self.adminUser.userName, "wrong" ), "Incorrect Password!","The password was wrong but login worked")


    def test_empty_inputs(self):
        #empty username
        self.assertEquals("No Username Provided!", myLogin.login(self.emptyUser.userName, self.emptyUser.password),"The username was empty but login worked")
        #empty password
        self.assertEquals("No Password Provided!", myLogin.login(self.standardUser.userName, self.emptyUser.password), "The password was empty but  worked")
        #both inputs empty
        self.assertEquals("No Username Provided!", myLogin.login(self.emptyUser.userName, self.emptyUser.password), "Both inputs were empty but login worked")

    def test_input_mismatch(self):
        self.assertEquals("Incorrect Password!", myLogin.login(self.adminUser.userName, self.standardUser.password),"The inputs don't match but login worked")


class CreateNewAccount(TestCase):

    myClient = None
    thingList = None

    def setUp(self):
        self.myClient = Client()
        self.thingList = {'flynnk': 'flynnPassword', 'smithj': 'smithPassword', 'petersont': "petersonPassword"}
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.myClient.post("/", {"userName": self.admin.userName, "password": self.admin.password})

        for i in self.thingList.keys():
            temp = myAccount(userName=i, password= self.thingList.get(i))
            temp.save()

    def test_unitTest_newAccount(self):
        errorMessage = createAccountFunctions.createAccount("williamsg", "williamsPassword", "Administrator")
        self.assertEqual("", errorMessage, "Failed to create account with valid inputs, username: williamsg password: williamsPassword")

    def test_unitTest_duplicateAccount(self):
        errorMessage = createAccountFunctions.createAccount("flynnk", "randomPassword", "Administrator")
        self.assertEqual("Username Already Exists!", errorMessage, "createAccount failed to produce error when trying to create a duplicate account, username: flynnk password: randomPassword")

    def test_unitTest_invalidAccountInput(self):
        errorMessage = createAccountFunctions.createAccount("", "randomPassword", "Administrator")
        self.assertEqual("No Username Provided!", errorMessage, "createAccount failed to produce error message with invalid inputs, username:  password: randomPassword")


class TestCase_empty_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_emptycreateCourse(self):
        errorMessage = createCourseFunctions.createCourse("", "")
        self.assertEqual("No Course Number or Course Name Provided!", errorMessage,"Creating a new course with empty fields. Expected errorMessage = 'No Course Number or Course Name Provided!'")

class TestCase_empty_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_empty_courseNumber_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("", "COMPSCI")
        self.assertEqual("No Course Number Provided!", errorMessage,"Creating a new course COMPSCI with number empty. Expected errorMessage = 'No Course Number Provided!'")

class TestCase_empty_courseName_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_empty_courseName_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "")
        self.assertEqual("No Course Name Provided!", errorMessage,"Creating a new empty course with number 1. Expected errorMessage = 'No Course Name Provided!'")

class TestCase_good_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_good_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCI")
        self.assertEqual("", errorMessage,"Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")

class TestCase_duplicate_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})
        self.compsciCourse = myCourse.objects.create(courseNumber="1", courseName="COMPSCI")

    def test_unit_duplicate_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCI")
        self.assertEqual("Course Number Already Exists!", errorMessage,"Creating a duplicate course COMPSCI with number 1. Expected errorMessage = 'Course Number Already Exists'")

class TestCase_badInput_courseNumber_notNumeric_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_badInput_courseNumber_notNumeric_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("asdf", "COMPSCI")
        self.assertEqual("Course Number Isn't Numeric!", errorMessage, "Creating a bad input course COMPSCI with number asdf. Expected errorMessage = 'Course Number Isn't Numeric'")

class TestCase_badInput_courseNumber_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_badInput_courseNumber_tooLong_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("99999999999", "COMPSCI")
        self.assertEqual("Course Number Is Too Long!", errorMessage,
                         "Creating a bad input too long course COMPSCI with number 99999999999. Expected errorMessage = 'Course Number Is Too Long!'")

class TestCase_badInput_courseName_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_badInput_courseName_tooLong_createCourse(self):
        errorMessage = createCourseFunctions.createCourse("1", "COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI")
        self.assertEqual("Course Name Is Too Long!", errorMessage, "Creating a bad input too long course COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI with number 1. Expected errorMessage = 'Course Name Is Too Long!'")


class testCreateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_createSection(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.assertEqual("", errorMessage, "Error creating new section")

class testDuplicateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.newLab = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_duplicateSection(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section 1")
        self.assertEqual("Lab Number Already Exists!", errorMessage,
                         "Error creating new section, labNumber already exists")

class testSectionInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_labNumberNumeric(self):
        errorMessage = createLabFunctions.createLab(labNumber="one", labName="Section 1")
        self.assertEqual("Lab Number Isn't Numeric!", errorMessage,
                         "Error creating new section, labNumber is not a number")

    def test_unit_labNumberTooLong(self):
        errorMessage = createLabFunctions.createLab(labNumber="11111111111", labName="Section 1")
        self.assertEqual("Lab Number Is Too Long!", errorMessage,
                         "Error creating new section, labNumber is greater than 10 characters")

    def test_unit_labNameTooLong(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="Section1Section1Section1")
        self.assertEqual("Lab Name Is Too Long!", errorMessage,
                         "Error creating new section, labName is greater than 20 characters")

class testSectionEmptyInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_unit_labNumberEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="", labName="Section 1")
        self.assertEqual("No Lab Number Provided!", errorMessage,
                         "Error creating new section, labNumber is empty")

    def test_unit_labNameEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="1", labName="")
        self.assertEqual("No Lab Name Provided!", errorMessage,
                         "Error creating new section, labName is empty")

    def test_unit_bothEmpty(self):
        errorMessage = createLabFunctions.createLab(labNumber="", labName="")
        self.assertEqual("No Lab Number or Lab Name Provided!", errorMessage,
                         "Error creating new section, both labNumber and labName are empty")

class TestCase_good_createLab(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unit_good_createLab(self):
        errorMessage = createLabFunctions.createLab("1", "COMPSCI")
        self.assertEqual("", errorMessage,"Creating a new lab COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")

class TestCase_duplicate_createLab(TestCase):
    def setUp(self):
        self.client = Client()
        self.compsciLab = myLab.objects.create(labNumber="1", labName="COMPSCI")

    def test_unit_duplicate_createCourse(self):
        errorMessage = createLabFunctions.createLab("1", "COMPSCI")
        self.assertEqual("Lab Number Already Exists!", errorMessage,"Creating a duplicate lab COMPSCI with number 1. Expected errorMessage = 'Lab Number Already Exists'")

class TestCase_badInput_createLab(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unit_badInput_createLab(self):
        errorMessage = createLabFunctions.createLab("asdf", "COMPSCI")
        self.assertEqual("Lab Number Isn't Numeric!", errorMessage,
                         "Creating a bad input lab COMPSCI with number asdf. Expected errorMessage = 'Lab Number Isn't Numeric'")


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName= "TA")
        self.course = myCourse.objects.create(courseName="MATH", courseNumber= 1,instructorUsername= "admin")
        self.assign = assignLabToCourse
        self.assignDuplicate = assignLabToCourse.assignLabToCourse(self.lab.LabNumber, self.course.courseNumber)

    def test_good_inputs(self):
        message = self.assign.assignLabToCourse(self.lab.LabNumber, self.course.courseNumber)
        self.assertEquals(message, "", "Assign lab to course failed. Expected the message <"">")

    def test_empty_inputs(self):
        # course Number empty
        message = self.assign.assignLabToCourse(self.lab.courseNumber, "")
        self.assertEquals(message, "No Course Number Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Course Number Provided!>")

        # lab Number empty
        message = self.assign.assignLabToCourse("", self.course.courseNumber)
        self.assertEquals(message, "No Lab Number Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Lab Number Provided!>")

        # Both inputs are invalid
        message = self.assign.assignLabToCourse("", "")
        self.assertEquals(message, "No Input Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Input Provided!>")

    def test_nonexisting_inputs(self):
        #non existing labNumber
        message = self.assign.assignLabToCourse("999", self.course.courseNumber)
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to course failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")
        # non existing courseNumber
        message = self.assign.assignLabToCourse(self.lab.LabNumber, "999")
        self.assertEquals(message, "This Course Doesn't Exist!", "Assign course to course failed. "
                                                              "Expected the message <This Course Doesn't Exist!>")
        # non existing labNumber and courseNumber
        message = self.assign.assignLabToCourse("999", "999")
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to course failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")

    def test_long_inputs(self):
        # long labNumber
        message = self.assign.assignLabToCourse("1000", self.course.courseNumber)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to course failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")
        # non existing courseNumber
        message = self.assign.assignLabToCourse(self.lab.LabNumber, "1000")
        self.assertEquals(message, "The Course Number Is Too Long!", "Assign course to course failed. "
                                                                 "Expected the message <The Course Number Is Too Long!>")
        # non existing labNumber and courseNumber
        message = self.assign.assignLabToCourse("1000", "1000")
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to course failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")

    def test_non_numeric_inputs(self):
        # non numeric labNumber
        message = self.assign.assignLabToCourse("lab", self.course.courseNumber)
        self.assertEquals(message, "The Lab Number Isn't Numeric!", "Assign lab to course failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")
        # non existing courseNumber
        message = self.assign.assignLabToCourse(self.lab.LabNumber, "course")
        self.assertEquals(message, "The Course Number Isn't Numeric!", "Assign course to course failed. "
                                                                 "Expected the message <The Course Number Isn't Numeric!>")
        # non existing labNumber and courseNumber
        message = self.assign.assignLabToCourse("lab", "course")
        self.assertEquals(message, "The Lab Number Isn't Numeric!", "Assign lab to course failed. "
                                                              "Expected the message <The Lab Number Isn't Numeric!>")

    def test_duplicate(self):
        message = self.assign.assignLabToCourse(self.lab.LabNumber, self.course.courseNumber)
        self.assertEquals(message, "These lab and course are already assigned", "Assign lab to course failed."
                                                "Expected the message <These lab and course are already assigned>")



class courseInstructorUnitTest(unittest.TestCase):
    def setUp(self):
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName= "TA")
        self.course = myCourse.objects.create(courseName="MATH", courseNumber= 1,instructorUsername= "admin")
        self.assign = assignLabToCourse
        self.assignDuplicate = assignLabToCourse.myCourseInstructor(self.myCourseInstructor.instructorUsername, self.myCourseInstructor.courseNumber)

    def testGoodInputs(self):
        message = self.assign.myCourseInstructor(self.myCourseInstructor.instructorUsername, self.course.courseNumber)
        self.assertEquals(message, "", "Assigning Instructor to course Succeeded. Expected the message <"">")

    def testEmptyInputs(self):
        # course Number field empty
        message = self.assign.myCourseInstructor(self.myCourseInstructor.courseNumber, "")
        self.assertEquals(message, "Course Number was Not Provided",
                          "Assigning instructor to course failed. Expected the message <Course Number was Not Provided>")

        # Instructor field empty
        message = self.assign.myCourseInstructor("", self.myCourseInstructor.courseNumber)
        self.assertEquals(message, "Instructor Name was Not Provided",
                          "Assigning instructor to course failed. Expected the message <Instructor Name was Not Provided>")

        # Both inputs are invalid
        message = self.assign.myCourseInstructor("", "")
        self.assertEquals(message, "No Instructor Name or Course Number Given", "Assigning Instructor to course failed. "
                                                         "Expected the message <No Instructor Name or Course Number Given>")

    def testNonexistingInputs(self):
        #Instructor doesn't exist
        message = self.assign.myCourseInstructor("DNE", self.myCourseInstructor.courseNumber)
        self.assertEquals(message,  "This Instructor Doesn't Exist",
                          "Assigning Instructor to course failed. Expected the message <This Instructor Doesn't Exist>")
        #courseNumber doesn't exist
        message = self.assign.myCourseInstructor(self.myCourseInstructor.instructorUsername, "999")
        self.assertEquals(message, "This Course Doesn't Exist",
                          "Assigning instructor to course failed. Expected the message <This Course Doesn't Exist>")
        # Both Instructor and Course Number don't Exist
        message = self.assign.myCourseInstructor("DNE", "999")
        self.assertEquals(message, "This Instructor and Course Don't Exist",
                          "Assigning instructor to course failed. Expected the message <This Instructor and Course Don't Exist>")

    def testLongInputs(self):
        # long InstructorUserName
        message = self.assign.myCourseInstructor("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", self.myCourseInstructor.instructorUsername)
        self.assertEquals(message, "Instructor Name is Too long",
                          "Assigning instructor to course failed. Expected the message <Instructor Name is Too long>")
        #long course number
        message = self.assign.myCourseInstructor(self.myCourseInstructor.instructorUsername, "1000")
        self.assertEquals(message, "Course Number is Too long",
                          "Assigning instructor to course failed. Expected the message <Course Number is Too long>")
        # long instructorUserName and long course number
        message = self.assign.myCourseInstructor("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "1000")
        self.assertEquals(message, "Instructor Name and Course Number are Too long",
                          "Assigning instructor to course failed. Expected the message <Instructor Name and Course Number are Too long>")

    def testTypeOfInputs(self):
        # non String Instructor
        message = self.assign.myCourseInstructor("951615", self.myCourseInstructor.courseNumber)
        self.assertEquals(message, "The Instructor name can't have numbers or special characters", "Assigning Instructor to course failed. "
                                                              "Expected the message <The Instructor name can't have numbers or special characters>")
        # non numeric courseNumber
        message = self.assign.myCourseInstructor(self.myCourseInstructor.instructorUsername, "number")
        self.assertEquals(message, "The Course Number Isn't Numeric", "Assigning Instructor to course failed. "
                                                                 "Expected the message <The Course Number Isn't Numeric>")
    def testDuplicateAssignment(self):
        message = self.assign.myCourseInstructor(self.myCourseInstructor.instructorUsername, self.myCourseInstructor.courseNumber)
        self.assertEquals(message, "This Instructor and course are already assigned", "Assigning Instructor to course failed."
                                                "Expected the message <This Instructor and course are already assigned>")


class AssignLabTAUnitTest(TestCase):
    def setUp(self):
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName="")
        self.ta = myAccount.objects.create(userName="kevin", password="pass", userType="TA")
        self.instructor = myAccount.objects.create(userName="Inst", password="pass", userType="Instructor")
        self.course = myCourse.objects.create(courseName="MATH", courseNumber="1",
                                              instructorUserName=self.instructor.userName)
        # assign the course to the instructor
        myCourseInstructor.objects.create(courseNumber=self.course.courseNumber,
                                          instructorUserName=self.instructor.userName)
        # assign the course to the lab
        labToCourse.objects.create(labNumber=self.lab.labNumber, courseNumber=self.course.courseNumber)

        self.assign = assignLabTA

    def test_good_inputs(self):
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_TA_with_multiple_lab(self):
        # assing this TA to another Lab
        # create a new lab
        newLab = myLab.objects.create(labName="LAB", labNumber="40", taUserName=self.ta.userName)
        # assign the course to the lab
        labToCourse.objects.create(labNumber=newLab.labNumber, courseNumber=self.course.courseNumber)

        message = self.assign.assignLabToTA(newLab.labNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_empty_inputs(self):
        # username empty
        message = self.assign.assignLabToTA(self.lab.labNumber, "", self.instructor.userName)
        self.assertEquals("No TA Username Provided!", message, "Assign lab to TA failed. "
                                                               "Expected the message <No TA Username Provided!>")
        # lab Number empty
        message = self.assign.assignLabToTA("", self.ta.userName, self.instructor.userName)
        self.assertEquals("No Lab Number Provided!", message, "Assign lab to course failed. "
                                                              "Expected the message <No Lab Number Provided!>")

        # instructor username empty
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, "")
        self.assertEquals("No Instructor Username Provided!", message, "Assign lab to course failed. "
                                                                       "Expected the message <No Instructor Username Number Provided!>")

        # all inputs are invalid
        message = self.assign.assignLabToTA("", "", "")
        self.assertEquals("No Input Provided!", message, "Assign lab to course failed. "
                                                         "Expected the message <No Input Provided!>")

    def test_non_existing_inputs(self):
        # non existing labNumber
        message = self.assign.assignLabToTA("999", self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")
        # non existing TA username
        message = self.assign.assignLabToTA(self.lab.labNumber, "aaa999", self.instructor.userName)
        self.assertEquals(message, "This TA Doesn't Exist!", "Assign course to TA failed. "
                                                             "Expected the message <This TA Doesn't Exist!>")

        # non existing instructor username
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, "aaa999")
        self.assertEquals(message, "This Instructor Doesn't Exist!", "Assign course to TA failed. "
                                                                     "Expected the message <This Instructor Doesn't Exist!>")

        # non existing labNumber , TA username and Instructor username
        message = self.assign.assignLabToTA("999", "aaa999", "aaa999")
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")

    def test_long_inputs(self):
        longUsername = "0123456789+012345678901234567890123456789qwertyuiop"
        longlabNumber = "1000"
        # long labNumber
        message = self.assign.assignLabToTA(longlabNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to TA failed. "
                                                                  "Expected the message <The Lab Number Is Too Long!>")
        # long instructor username
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, longUsername)
        self.assertEquals(message, "The Instructor Username Is Too Long!", "Assign lab to TA failed. "
                                        "Expected the message <The Instructor Username Is Too Long!>")
        # non existing username
        message = self.assign.assignLabToTA(self.lab.labNumber, longUsername, self.instructor.userName)
        self.assertEquals(message, "The TA Username Is Too Long!", "Assign lab to TA failed. "
                                        "Expected the message <The TA Username Is Too Long!>")
        # non existing labNumber and username
        message = self.assign.assignLabToTA(longlabNumber, longUsername, longUsername)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to TA failed. "
                                        "Expected the message <The Lab Number Is Too Long!>")

    def test_non_numeric_labNumber(self):
        # non numeric labNumber
        message = self.assign.assignLabToTA("lab", self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "Lab Number Isn't Numeric!", "Assign lab to TA failed. "
                            "Expected the message <Lab Number Is Too Long!>")

    def test_duplicate(self):
        self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, self.instructor.userName)
        # create a duplicate
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals("This Lab Already Has A TA!", message, "Assign lab to TA failed."
                                                                "Expected the message <This Lab Already Has A TA!>")

    def test_multiple_TA(self):
        self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, self.instructor.userName)
        # assign a different TA to an already assigned Lab
        newTA = myAccount.objects.create(userName="new", password="0000", userType="TA")
        message = self.assign.assignLabToTA(self.lab.labNumber, newTA.userName, self.instructor.userName)
        self.assertEquals("This Lab Already Has A TA!", message, "Assign lab to TA failed."
                                                "Expected the message <This Lab Already Has A TA!>")

    def test_correct_instructor(self):
        instructor = myAccount.objects.create(userName="jrock", password="millyRock", userType="Instructor")
        course = myCourse.objects.create(courseName="Dance", courseNumber="101",
                                         instructorUserName=instructor.userName)
        lab = myLab.objects.create(labName="DanceLab", labNumber="202", taUserName="")
        # assign instructor to course
        myCourseInstructor.objects.create(courseNumber=course.courseNumber, instructorUserName=instructor.userName)
        # assign the lab to the course
        labToCourse.objects.create(labNumber=lab.labNumber, courseNumber=course.courseNumber)
        # check the TA to the lab
        message = self.assign.assignLabToTA(lab.labNumber, self.ta.userName, instructor.userName)
        self.assertEquals("", message, "Assign lab to TA failed. Expected the message <"">")

    def test_unauthorized_assignment(self):
        # try to assign a TA to a course with an instructor has not been assigned to the course
        impostor = myAccount.objects.create(userName="thief", password="password", userType="Instructor")
        # setup a course and a lab for the instructor
        course = myCourse.objects.create(courseName="Dance", courseNumber="101",
                                         instructorUserName=impostor.userName)
        lab = myLab.objects.create(labName="DanceLab", labNumber="85", taUserName="")
        myCourseInstructor.objects.create(courseNumber=course.courseNumber, instructorUserName=impostor.userName)
        labToCourse.objects.create(labNumber=lab.labNumber, courseNumber=course.courseNumber)
        # check the TA to the lab
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, impostor.userName)
        self.assertEquals("Unauthorized Assignment!", message, "Assign lab to TA failed. "
                                                               "Expected the message <Unauthorized Assignment>")

    def test_instructor_without_course(self):
        instructorNoCourse = myAccount.objects.create(userName="jrock", password="millyRock", userType="Instructor")
        # check assigning the TA to the lab with the instructor that doesn;t have a course
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, instructorNoCourse.userName)
        self.assertEquals("This Instructor Doesn't Have A Course!", message, "Assign lab to TA failed. "
                                                                             "Expected the message <This Instructor Doesn't Have A Course!>")

    def test_admin_privileges(self):
        admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        # assign TA to Lab with the admin account
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, admin.userName)
        self.assertEquals("", message, "Assign lab to TA failed. Expected the message<"">")

