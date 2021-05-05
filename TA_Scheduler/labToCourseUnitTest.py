import unittest
from django.test import TestCase
from django.test import Client
from .models import myLab
from .models import myCourse
import sys
from .assignLabToCourse import assignLabToCourse

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
if __name__ == '__main__':
    unittest.main()
