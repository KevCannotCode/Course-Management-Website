from django.test import TestCase, Client
from .models import myAccount, myCourse, myLab, myContact, myCourseInstructor, myLabTA, labToCourse

class login_test(TestCase):

    def setUp(self):
        #Setup client, account and something in the list
        self.client = Client()
        self.adminUser = myAccount.objects.create(userName="admin", password="password")
        self.standardUser = myAccount.objects.create(userName="dude", password = "pass")
        self.emptyUser = myAccount.objects.create(userName= "", password= "" )
        #create a course

    def test_good_login(self):
        #Good login with admin
        response = self.client.post("/", {"userName": self.adminUser.userName, "password": self.adminUser.password})
        #Check redirect: Should it redirect to a homepge when the user logs in?
        self.assertEqual("/home/", response.url,"Log in as admin with correct credentials admin failed."
                                                    "Expected redirect URL to be /home")
        #Good login with standard user
        response = self.client.post("/", {"userName": self.standardUser.userName, "password": self.standardUser.password})
        #Check redirect: Should it redirect to a homepge when the user logs in?
        self.assertEqual("/home/", response.url,"Log in a standard user with correct credentials admin failed."
                                                    "Expected redirect URL to be /home")

    def test_empty_credentials(self):
        #Login with an empty username
        response = self.client.post("/", {"userName": self.standardUser.userName, "password": self.emptyUser.password})
        self.assertEqual("No Password Provided!", response.context['errorMessage'],
        "Log in with an empty password should fail. Expected <No Password Provided!> message")
        # Login with an empty password
        response = self.client.post("/", {"userName": self.emptyUser.userName, "password": self.emptyUser.password})
        self.assertEqual("No Username Provided!", response.context['errorMessage'],
                         "Log in with an empty password should fail. Expected <No Username Provided!> message")
        #login with empty username and password
        response = self.client.post("/", {"userName": self.emptyUser.userName, "password": self.emptyUser.password})
        self.assertEqual("No Username Provided!", response.context['errorMessage'],"Log in with an empty "
        "password and username should fail. Expected <No Username Provided!> message")

    def test_inexisting_credentials(self):
        #Login with an inexisting username
        response = self.client.post("/", {"userName": "ret8578", "password": self.standardUser.password })
        self.assertEqual("User Doesn't Exist", response.context['errorMessage'],
        "Log in with an incorrect username. Expected <User Doesn't Exist> message")
        # Login with an inexisting username
        response = self.client.post("/", {"userName": "ret8578", "password": self.adminUser.password})
        self.assertEqual("User Doesn't Exist", response.context['errorMessage'],
                         "Log in with an incorrect username. Expected <User Doesn't Exist> message")

        # Login with an inexisting password
        response = self.client.post("/", {"userName": self.standardUser.userName, "password": "eddee"})
        self.assertEqual("Incorrect Password!", response.context['errorMessage'],
                         "Log in with an incorrect password. Expected <Incorrect Password!> message")
        # Login with an inexisting username
        response = self.client.post("/", {"userName": self.adminUser.userName, "password": "eddee"})
        self.assertEqual("Incorrect Password!", response.context['errorMessage'],
                         "Log in with an incorrect password. Expected <Incorrect Password!> message")

    def test_unmatching_credentials(self):#we test existing username and password that do not match
        #Login with a standard username and admin password
        response = self.client.post("/", {"userName": self.standardUser.userName, "password": self.adminUser.password })
        self.assertEqual("Incorrect Password!", response.context['errorMessage'],
        "Log in with an incorrect password. Expected <Incorrect Password!> message")
        # Login with a standard password and admin username
        response = self.client.post("/", {"userName": self.adminUser.userName, "password": self.standardUser.password})
        self.assertEqual("Incorrect Password!", response.context['errorMessage'],
                         "Log in with an incorrect password. Expected <Incorrect Password!> message")


class CreateNewAccount(TestCase):

    def setUp(self):
        self.myClient = Client()
        self.thingList = {'flynnk': 'flynnPassword', 'smithj': 'smithPassword', 'petersont': "petersonPassword"}
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.myClient.post("/", {"userName": self.admin.userName, "password": self.admin.password})

        for i in self.thingList.keys():
            temp = myAccount(userName=i, password= self.thingList.get(i))
            temp.save()

    def test_acceptanceTest_newAccount(self):
        resp = self.myClient.post("/create-account/", {"userName": "jacksonl", "password" : "jacksonlPassword", "userType": "Administrator"})
        self.assertEqual("", resp.context["errorMessage"], "new account not created, user:todd, pass:toddPassword")

    def test_acceptanceTest_UsernameUsed(self):
        for i in self.thingList.keys():
            resp = self.myClient.post("/create-account/", {"userName": i, "password": self.thingList.get(i), "userType": "Administrator"})
            self.assertEqual("Username Already Exists!", resp.context["errorMessage"], "not stopped from creating duplicate account")

    def test_acceptanceTest_invalidAccountInput(self):
        resp = self.myClient.post("/create-account/", {"userName": "", "password": "randomPassword", "userType": "Administrator"})
        self.assertEqual("No Username Provided!", resp.context["errorMessage"], "system allowed an invalid input for account creation")



class TestCase_empty_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "", "courseName": ""})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Number or Course Name Provided!", response.context["errorMessage"],"Creating a new course with empty fields. Expected errorMessage = 'No Course Number or Course Name Provided!'")


class TestCase_empty_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "", "courseName": ""})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Number or Course Name Provided!", response.context["errorMessage"],"Creating a new course with empty fields. Expected errorMessage = 'No Course Number or Course Name Provided!'")


class TestCase_empty_courseName_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_empty_courseName_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": ""})
        course_list = response.context["course_list"]
        self.assertEqual("No Course Name Provided!", response.context["errorMessage"],"Creating a new empty course with number 1. Expected errorMessage = 'No Course Name Provided!'")


class TestCase_good_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_good_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        course_list = response.context["course_list"]
        coursePair = course_list[0]
        self.assertEqual("1", str(coursePair[0]),"Creating a new course COMPSCI with number 1 failed. Expected course numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(coursePair[1]),"Creating a new course COMPSCI with number 1 failed. Expected course names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],"Creating a new course COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")


class TestCase_duplicate_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})
        self.compsciCourse = myCourse.objects.create(courseNumber="1", courseName="COMPSCI")

    def test_acceptance_duplicate_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCI"})
        self.assertEqual("Course Number Already Exists!", response.context["errorMessage"],"Creating a duplicate course COMPSCI with number 1. Expected errorMessage = 'Course Number Already Exists'")

    class TestCase_badInput_courseNumber_notNumeric_createCourse(TestCase):
        def setUp(self):
            self.client = Client()
            self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
            self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

        def test_acceptance_badInput_courseNumber_notNumeric_createCourse(self):
            response = self.client.post("/create-course/", {"courseNumber": "asdf", "courseName": "COMPSCI"})
            self.assertEqual("Course Number Isn't Numeric!", response.context["errorMessage"],
                             "Creating a bad input course COMPSCI with number asdf. Expected errorMessage = 'Course Number Isn't Numeric'")


class TestCase_badInput_courseNumber_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_badInput_courseNumber_tooLong_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "99999999999", "courseName": "COMPSCI"})
        self.assertEqual("Course Number Is Too Long!", response.context["errorMessage"],
                         "Creating a bad input too long course COMPSCI with number 99999999999. Expected errorMessage = 'Course Number Is Too Long!'")


class TestCase_badInput_courseName_tooLong_createCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_badInput_courseName_tooLong_createCourse(self):
        response = self.client.post("/create-course/", {"courseNumber": "1", "courseName": "COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI"})
        self.assertEqual("Course Name Is Too Long!", response.context["errorMessage"],
                         "Creating a bad input too long course COMPSCICOMPSCICOMPSCICOMPSCICOMPSCICOMPSCI with number 1. Expected errorMessage = 'Course Name Is Too Long!'")


class TestCase_good_createLab(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_good_createLab(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "COMPSCI"})
        lab_list = response.context["lab_list"]
        labPair = lab_list[0]
        self.assertEqual("1", str(labPair[0]),"Creating a new lab COMPSCI with number 1 failed. Expected lab numbers to match. 1 = 1")
        self.assertEqual("COMPSCI", str(labPair[1]),"Creating a new lab COMPSCI with number 1 failed. Expected lab names to match. COMPSCI = COMPSCI")
        self.assertEqual("", response.context["errorMessage"],"Creating a new lab COMPSCI with number 1 failed. Expected errorMessage to be empty. '' = '' ")


class TestCase_duplicate_createLab(TestCase):
    def setUp(self):
        self.client = Client()
        self.compsciLab = myLab.objects.create(labNumber="1", labName="COMPSCI")
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_duplicate_createLab(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "COMPSCI"})
        self.assertEqual("Lab Number Already Exists!", response.context["errorMessage"],"Creating a duplicate lab COMPSCI with number 1. Expected errorMessage = 'Lab Number Already Exists'")

    class TestCase_badInput_createLab(TestCase):
        def setUp(self):
            self.client = Client()

        def test_acceptance_badInput_createLab(self):
            response = self.client.post("/create-lab/", {"courseNumber": "asdf", "labName": "COMPSCI"})
            self.assertEqual("Lab Number Isn't Numeric", response.context["errorMessage"],
                             "Creating a bad input lab COMPSCI with number asdf. Expected errorMessage = 'Lab Number Isn't Numeric'")


class labToCourse_acceptance_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.lab = myLab.objects.create(labName= "MATHLAB", labNumber="202", taUserName= "TA")
        self.course = myCourse.objects.create(courseName= "MATH", courseNumber= 1)
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})


    def test_good_assign(self):
        response = self.client.post("/assign-LabToCourse/", {"courseNumber": 1, "labNumber": 202})
        self.assertEqual("", response.context["errorMessage"], "Failed to assign lab to course")

    def test_empty_arguments(self):
        self.assertEquals()

class testCreateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_createSection(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section 1"})
        lab_list = response.context["lab_list"]
        testLab = lab_list[0]
        self.assertEqual("1", str(testLab[0]), "New section creation failed at sectionNumber")
        self.assertEqual("Section 1", str(testLab[1]), "New section creation failed at sectionName")
        self.assertEqual("", response.context["errorMessage"],
                         "Error creating new section")


class testDuplicateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.newLab = myLab.objects.create(labNumber="1", labName="Section 1")
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_duplicateSection(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section 1"})
        self.assertEqual("Lab Number Already Exists!", response.context["errorMessage"],
                         "Error creating new section, labNumber already exists")


class testSectionInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_labNumberNumeric(self):
        response = self.client.post("/create-lab/", {"labNumber": "one", "labName": "Section 1"})
        self.assertEqual("Lab Number Isn't Numeric!", response.context["errorMessage"],
                         "Error creating new section, labNumber is not a number")

    def test_acceptance_labNumberTooLong(self):
        response = self.client.post("/create-lab/", {"labNumber": "11111111111", "labName": "Section 1"})
        self.assertEqual("Lab Number Is Too Long!", response.context["errorMessage"],
                         "Error creating new section, labNumber is greater than 10 characters")

    def test_acceptance_labNameTooLong(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": "Section1Section1Section1"})
        self.assertEqual("Lab Name Is Too Long!", response.context["errorMessage"],
                         "Error creating new section, labName is greater than 20 characters")


class testSectionEmptyInput(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = myAccount.objects.create(userName="admin", password="password", userType="Administrator")
        self.client.post("/", {"userName": self.admin.userName, "password": self.admin.password})

    def test_acceptance_labNumberEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "", "labName": "Section 1"})
        self.assertEqual("No Lab Number Provided!", response.context["errorMessage"],
                         "Error creating new section, labNumber is empty")

    def test_acceptance_labNameEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "1", "labName": ""})
        self.assertEqual("No Lab Name Provided!", response.context["errorMessage"],
                         "Error creating new section, labName is empty")

    def test_acceptance_bothEmpty(self):
        response = self.client.post("/create-lab/", {"labNumber": "", "labName": ""})
        self.assertEqual("No Lab Number or Lab Name Provided!", response.context["errorMessage"],
                         "Error creating new section, both labNumber and labName are empty")



class myCourseInstructor(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = myCourseInstructor.objects.create(instructorUsername= "admin", courseNumber= 1)

    def testGoodArgs(self):
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": self.myCourseInstructor.instructorUserName,
                                                         "CourseNumber": self.myCourseInstructor.courseNumber})
        self.assertEquals(resp.context["message"], "Course Assigned", "assigning instructor to course succeeded."
                                                                   "Expected <Course Assigned> message")

    def testEmptyArgs(self):
        #empty instructorUserName
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": "", "course Number:": self.myCourseInstructor.courseNumber})
        self.assertEquals(resp.context["message"], "Instructor Name was Not Provided",
                          "Assigning instructor to course failed. Expected the message <Instructor Name was Not Provided>")
        # empty courseNumber
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": self.myCourseInstructor.instructorUserName, "course Number":""})
        self.assertEquals(resp.context["message"], "Course Number was Not Provided",
                          "Assigning instructor to course failed. Expected the message <Course Number was Not Provided>")
        # empty instructorUserName and courseNumber
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": "", "course Number:": ""})
        self.assertEquals(resp.context["message"], "Both Instructor and Course number are required",
                          "Assigning instructor to course failed. Expected the message <Both Instructor and Course number are required>")

    def testLongArgs(self):
        #long instructorUserName
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "course Number:":self.myCourseInstructor.courseNumber})
        self.assertEquals(resp.context["message"], "Instructor Name is Too long",
                          "Assigning instructor to course failed. Expected the message <Instructor Name is Too long>")
        #long course number
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": self.myCourseInstructor.instructorUserName,"course Number:": "7410"})
        self.assertEquals(resp.context["message"], "Course Number is Too long",
                          "Assigning instructor to course failed. Expected the message <Course Number is Too long>")
        #long instructorUserName and long course number
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "course Number:": "7410"})
        self.assertEquals(resp.context["message"], "Instructor Name and Course Number are Too long",
                          "Assigning instructor to course failed. Expected the message <Instructor Name and Course Number are Too long>")

    def testNumbersMax(self):

        # max course number
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": self.myCourseInstructor.instructorUserName, "course Number:":sys.maxsize})
        self.assertEquals(resp.context["message"], "Course Number is too Large",
                          "Assigning instructor to course failed. Expected the message <Course Number is too Large>")
        # min course number
        resp = self.client.post("/assign-course-instructor/",
                                {"Instructor Name:": self.myCourseInstructor.instructorUserName, "course Number:": -sys.maxsize+1})
        self.assertEquals(resp.context["message"], "Course Number must be >0",
                          "Assigning instructor to course failed. Expected the message <Course Number must be >0>")

    def testNonexistingArgs(self):
        # Non-existing Instructor but good course number
        resp = self.client.post("/assign-course-instructor/",
                                {"Instructor Name:": "DNE", "course Number:": self.myCourseInstructor.courseNumber})
        self.assertEquals(resp.context["message"], "This Instructor Doesn't Exist",
                          "Assigning Instructor to course failed. Expected the message <This Instructor Doesn't Exist>")
        # Good Instructor but non existing course number
        resp = self.client.post("/assign-course-instructor/",
                                {"Instructor Name:": self.myCourseInstructor.instructorUserName, "course Number:": "999"})
        self.assertEquals(resp.context["message"], "This Course Doesn't Exist",
                          "Assigning instructor to course failed. Expected the message <This Course Doesn't Exist>")
        # Both Instructor and Course Number don't Exist
        resp = self.client.post("/assign-course-instructor/", {"Instructor Name:": "DNE", "course Number:": "999"})
        self.assertEquals(resp.context["message"], "This Instructor and Course Don't Exist",
                          "Assigning instructor to course failed. Expected the message <This Instructor and Course Don't Exist>")
