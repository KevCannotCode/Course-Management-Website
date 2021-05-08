import unittest
from .models import myLab
from .models import myAccount
from .models import myLabTA
from .assignLabTA import assignLabTA

class AssignLabTAUnitTest(unittest.TestCase):
    def setUp(self):
        self.lab = myLab.objects.create(labName="MATHLAB", labNumber="202", taUserName= "kevin")
        self.ta = myAccount.objects.create(userName="kevin", password= "pass", userType= "TA")
        self.assign = assignLabTA

    def test_good_inputs(self):
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")
        #assing this TA to another Lab
        newLab = myLab.objects.create(labName= "LAB", labNumber= "40", taUserName= self.ta.userName)
        message = self.assign.assignLabToTA(newLab.labNumber, self.ta.userName)
        self.assertEquals(message, "", "Assign lab to TA failed. Expected the message <"">")

    def test_empty_inputs(self):
        # username empty
        message = self.assign.assignLabToTA(self.lab.labNumber, "")
        self.assertEquals(message, "No Username Provided!", "Assign lab to TA failed. "
                                                         "Expected the message <No Username Provided!>")
        # lab Number empty
        message = self.assign.assignLabToTA("", self.ta.username)
        self.assertEquals(message, "No Lab Number Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Lab Number Provided!>")

        # Both inputs are invalid
        message = self.assign.assignLabToTA("", "")
        self.assertEquals(message, "No Input Provided!", "Assign lab to course failed. "
                                                         "Expected the message <No Input Provided!>")

    def test_non_existing_inputs(self):
        #non existing labNumber
        message = self.assign.assignLabToTA("999", self.ta.userName)
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")
        # non existing username
        message = self.assign.assignLabToTA(self.lab.LabNumber, "aaa999")
        self.assertEquals(message, "This TA Doesn't Exist!", "Assign course to TA failed. "
                                                              "Expected the message <This TA Doesn't Exist!>")
        # non existing labNumber and username
        message = self.assign.assignLabToTA("999", "999")
        self.assertEquals(message, "This Lab Doesn't Exist!", "Assign lab to TA failed. "
                                                              "Expected the message <This Lab Doesn't Exist!>")

    def test_long_inputs(self):
        longUsername = "0123456789+012345678901234567890123456789qwertyuiop"
        longLabNumber = "1000"
        # long labNumber
        message = self.assign.assignLabToTA(longLabNumber, self.ta.userName)
        self.assertEquals(message, "The Lab Number Is Too Long!", "Assign lab to TA failed. "
                                                              "Expected the message <The Lab Number Is Too Long!>")
        # non existing username
        message = self.assign.assignLabToTA(self.lab.LabNumber, longUsername)
        self.assertEquals(message, "The username Is Too Long!", "Assign lab to TA failed. "
                                                                 "Expected the message <The Course Number Is Too Long!>")
        # non existing labNumber and username
        message = self.assign.assignLabToTA(longLabNumber, longUsername)
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
        message = self.assign.assignLabToTA(self.lab.LabNumber, self.course.courseNumber)
        self.assertEquals(message, "This Lab Already Has a TA", "Assign lab to course failed."
                                                "Expected the message <This Lab Already Has a TA>")
    def test_multiple_TA(self):
        self.assign.assignLabToTA(self.lab.LabNumber, self.ta.userName)
        #assign a different TA to an already assigned Lab
        newTA = myAccount.objects.create(userName= "new", password= "0000", userType= "TA")
        message = self.assign.assignLabToTA(self.lab.LabNumber, newTA.userName)
        self.assertEquals(message, "This Lab Already Has a TA", "Assign lab to course failed."
                                                "Expected the message <This Lab Already Has a TA>")
