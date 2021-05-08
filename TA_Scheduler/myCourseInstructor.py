from django.test import TestCase
from django.test import Client
from .models import myCourseInstructor


class myCourseInstructor:
    def myCourseInstructor( instructorUserName , courseNumber):
        # check the validity of input
        errorMessage = myCourseInstructor.inputValidation(instructorUserName, courseNumber)
        # check if the instructor and course already exist
        errorMessage = myCourseInstructor.DatabaseCheck(instructorUserName, courseNumber)

        if errorMessage == "":
            # checks if there is an existing courseInstructor entry
            entry = list(myCourseInstructor.objects.filter(instructorUserName=instructorUserName, courseNumber=courseNumber))
            if len(entry) != 0:
                errorMessage = "This instructor and course is assigned already"
                return errorMessage
            # if there is no existing entry, then we can assign it
            assign = myCourseInstructor(instructorUserName=instructorUserName, courseNumber=courseNumber)
            assign.save()

        return errorMessage

    def inputValidation(instructorUserName, courseNumber):
        errorMessage = ""
        # Check for empty inputs
        if len(instructorUserName) < 1:
            errorMessage = "Instructor name is required"
            return errorMessage
        elif len(courseNumber) < 1:
            errorMessage = "Course number is required"
            return errorMessage

        # Check for long inputs
        elif len(instructorUserName) > 40:
            errorMessage = "The Lab Number Is Too Long!"
            return errorMessage

        elif len(courseNumber) > 3:
            errorMessage = "The Course number can only be up to 3 digits long"
            return errorMessage

        # Check for numeric input
        elif not (courseNumber.isnumeric()):
            errorMessage = "The course number isn't a number"
        return errorMessage

    def DatabaseCheck(instructorUserName, courseNumber):
        errorMessage = ""
        try:
            instructor = myCourseInstructor.objects.filter(instructorUserName=instructorUserName)
        except myCourseInstructor.DoesNotExist:
            errorMessage = "The instructor does not exist"
        try:
            course = myCourseInstructor.objects.filter(courseNumber=courseNumber)
        except myCourseInstructor.DoesNotExist:
            errorMessage = "The course does not exist"
        finally:
            return errorMessage






