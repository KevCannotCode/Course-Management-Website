from django.test import TestCase
from django.test import Client
from .models import myCourseInstructor
from .models import myAccount
from .models import myCourse

class myCourseInstructor:
    def myCourseInstructor( instructorUserName , courseNumber):
        # check the validity of input
        errorMessage = myCourseInstructor.inputValidation(instructorUserName, courseNumber)
        # check if the instructor and course already exist
        if errorMessage == "":
            errorMessage = myCourseInstructor.DatabaseCheck(instructorUserName, courseNumber)

        if errorMessage == "":
            assign = myCourseInstructor(instructorUserName=instructorUserName, courseNumber=courseNumber)
            assign.save()
        return errorMessage

    def inputValidation(instructorUserName, courseNumber):
        errorMessage = ""
        # Check for empty inputs
        if len(instructorUserName) < 1 and len(courseNumber) < 1:
            errorMessage = "No Input Provided!"
            return errorMessage
        if len(instructorUserName) < 1:
            errorMessage = "Instructor name is required"
            return errorMessage
        elif len(courseNumber) < 1:
            errorMessage = "Course number is required"
            return errorMessage

        # Check for long inputs
        elif len(instructorUserName) > 40:
            errorMessage = "Instructor Name is Too long!"
            return errorMessage

        elif len(courseNumber) > 3:
            errorMessage = "The Course number can only be up to 3 digits long"
            return errorMessage

        # Check for numeric input
        elif not (courseNumber.isnumeric()):
            errorMessage = "The Course Number Isn't Numeric!"
        return errorMessage

    def DatabaseCheck(instructorUserName, courseNumber):
        errorMessage = ""

        instructor = myAccount.objects.filter(userName=instructorUserName)
        if len(instructor) < 1:
            errorMessage = "The instructor does not exist"
            return errorMessage
        course = myCourse.objects.filter(courseNumber=courseNumber)
        if len(course) < 1:
            errorMessage = "This Course Doesn't Exist"
            return errorMessage
        instructor = myCourseInstructor.objects.filter(instructorUserName= instructorUserName)
        if len(instructor) < 1:
            errorMessage = "The Instructor Has Already Been assigned!"
            return errorMessage
        course = myCourseInstructor.objects.filter(courseNumber=courseNumber)
        if len(course) < 1:
            errorMessage = "This Course Has Already Been Assigned!"
            return errorMessage
        instructorToCourse = myCourseInstructor.objects.filter(instructorUserName= instructorUserName
                                                               ,courseNumber= courseNumber)
        if len(instructorToCourse) < 1:
            errorMessage = "This Instructor Has Already Been Assigned To This Course!"
            return errorMessage
        return errorMessage





