import unittest
from .models import myLab
from .models import myAccount
from .models import myLabTA
from .assignLabTA import assignLabTA
from .models import myCourseInstructor
from .models import myCourse
from .models import labToCourse

class AssignLabTAUnitTest(unittest.TestCase):
    def setUp(self):
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName="")
        self.ta = myAccount.objects.create(userName="kevin", password="pass", userType="TA")
        self.instructor = myAccount.objects.create(userName="Inst", password= "pass", userType= "Instructor")
        self.course = myCourse.objects.create(courseName= "MATH", courseNumber= "1",
                                              instructorUserName= self.instructor.userName)
        #assign the course to the instructor
        myCourseInstructor.objects.create(courseNumber= self.course.courseNumber,
                                          instructorUserName= self.instructor.userName)
        #assign the course to the lab
        labToCourse.objects.create(labNumber= self.lab.labNumber, courseNumber= self.course.courseNumber)

        self.assign = assignLabTA

    def test_good_inputs(self):
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_TA_with_multiple_lab(self):
        #assing this TA to another Lab
        # create a new lab
        newLab = myLab.objects.create(labName= "LAB", labNumber= "40", taUserName= self.ta.userName)
        # assign the course to the lab
        labToCourse.objects.create(labNumber=newLab.labNumber, courseNumber=self.course.courseNumber)

        message = self.assign.assignLabToTA(newLab.labNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_empty_inputs(self):
        # username empty
        message = self.assign.assignLabToTA(self.lab.labNumber, "", self.instructor.userName)
        self.assertEquals(message, "No TA Username Provided!", "Assign lab to TA failed. "
                                                         "Expected the message <No TA Username Provided!>")
        # lab Number empty
        message = self.assign.assignLabToTA("", self.ta.username, self.instructor.userName)
        self.assertEquals(message, "No Lab Number Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Lab Number Provided!>")

        # instructor username empty
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.username, "")
        self.assertEquals(message, "No Instructor Username Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Instructor Username Number Provided!>")

        # all inputs are invalid
        message = self.assign.assignLabToTA("", "", "")
        self.assertEquals(message, "No Input Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Input Provided!>")

    def test_non_existing_inputs(self):
        #non existing labNumber
        message = self.assign.assignLabToTA("999", self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")
        # non existing TA username
        message = self.assign.assignLabToTA(self.lab.LabNumber, "aaa999", self.instructor.userName)
        self.assertEquals(message, "This TA Doesn't Exist!", "Assign course to TA failed. "
                                                              "Expected the message <This TA Doesn't Exist!>")

        # non existing instructor username
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName ,"aaa999")
        self.assertEquals(message, "This Instructor Doesn't Exist!", "Assign course to TA failed. "
                                                             "Expected the message <This Instructor Doesn't Exist!>")

        # non existing labNumber , TA username and Instructor username
        message = self.assign.assignLabToTA("999", "aaa999", "aaa999")
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")

    def test_long_inputs(self):
        longUsername = "0123456789+012345678901234567890123456789qwertyuiop"
        longLabNumber = "1000"
        # long labNumber
        message = self.assign.assignLabToTA(longLabNumber, self.ta.userName, self.instructor.userName)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to TA failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")
        # long instructor username
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName, longUsername)
        self.assertEquals(message, "The Instructor Username Is Too Long!", "Assign lab to TA failed. "
                                                              "Expected the message <The Instructor Username Is Too Long!>")
        # non existing username
        message = self.assign.assignLabToTA(self.lab.LabNumber, longUsername, self.instructor.userName)
        self.assertEquals(message, "The TA username Is Too Long!", "Assign lab to TA failed. "
                                                                 "Expected the message <The TA Username Is Too Long!>")
        # non existing labNumber and username
        message = self.assign.assignLabToTA(longLabNumber, longUsername, longUsername)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to TA failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")

    def test_non_numeric_labNumber(self):
        # non numeric labNumber
        message = self.assign.assignLabToTA("lab", self.ta.userName)
        self.assertEquals(message, "The Lab Number Isn't Numeric!", "Assign lab to TA failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")

    def test_duplicate(self):
        self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName)
        #create a duplicate
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.course.courseNumber, self.instructor.userName)
        self.assertEquals(message, "This Lab Already Has a TA", "Assign lab to TA failed."
                                                "Expected the message <This Lab Already Has a TA>")
    def test_multiple_TA(self):
        self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName, self.instructor.userName)
        #assign a different TA to an already assigned Lab
        newTA = myAccount.objects.create(userName= "new", password= "0000", userType= "TA")
        message = self.assign.assignLabToTA(self.lab.LabNumber, newTA.userName, self.instructor.userName)
        self.assertEquals(message, "This Lab Already Has a TA", "Assign lab to TA failed."
                                                "Expected the message <This Lab Already Has a TA>")

    def test_correct_instructor(self):
        instructor = myAccount.objects.create(userName= "jrock", password= "millyRock", userType= "Instructor")
        course = myCourse.objects.create(courseName= "Dance", courseNumber= "101",
                                         instructorUserName= instructor.userName)
        lab = myLab.objects.create(labName= "DanceLab", labNumber= "202", taUserName= "")
        #assign instructor to course
        myCourseInstructor.objects.create(courseNumber= course.courseNumber, instructorUserName= instructor.userName)
        #assign the lab to the course
        labToCourse.objects.create(labNumber= lab.labNumber, courseNumber= course.courseNumber)
        #check the TA to the lab
        message = self.assign.assignLabToTA(lab.labNumber, self.ta.userName,instructor.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_unauthorized_assignment(self):
        #try to assign a TA to a course with an instructor has not been assigned to the course
        impostor = myAccount.objects.create(userName= "thief", password= "password", userType= "Instructor")
        # setup a course and a lab for the instructor
        course = myCourse.objects.create(courseName= "Dance", courseNumber= "101",
                                         instructorUserName= impostor.userName)
        lab = myLab.objects.create(labName= "DanceLab", labNumber= "202", taUserName= "")
        myCourseInstructor.objects.create(courseNumber= course.courseNumber, instructorUserName= impostor.userName)
        labToCourse.objects.create(labNumber= lab.labNumber, courseNumber= course.courseNumber)
        #check the TA to the lab
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, impostor.userName)
        self.assertEquals(message, "Unauthorized Assignment!", "Assign lab to TA failed. "
                                            "Expected the message <Unauthorized Assignment>")

    def test_instructor_without_course(self):
        instructorNoCourse = myAccount.objects.create(userName="jrock", password="millyRock", userType="Instructor")
        # check assigning the TA to the lab with the instructor that doesn;t have a course
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, instructorNoCourse.userName)
        self.assertEquals(message, "This Instructor Doesn't Have A Course!", "Assign lab to TA failed. "
                                        "Expected the message <This Instructor Doesn't Have A Course!>")

    def test_admin_privileges(self):
        admin = myAccount.objects.create(userName = "admin", password= "password", userType= "Administrator")
        # assign TA to Lab with the admin account
        message = self.assign.assignLabToTA(self.lab.labNumber, self.ta.userName, admin.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message<"">")
