from .models import labToCourse
from .models import myLab
from .models import myCourse

class assignLabToCourse:
    def assignLabToCourse(labNumber, courseNumber):
        #check the validity of the inputs
        errorMessage = assignLabToCourse.inputValidation(labNumber, courseNumber)
        #check if the lab and course exist
        if errorMessage == "":
            errorMessage = assignLabToCourse.retrieveInDatabase(labNumber, courseNumber)

        if errorMessage == "":
            #check if there are any existing labTocourse entry
            entry = list(labToCourse.objects.filter(labNumber=labNumber) )
            if len(entry) != 0:
                errorMessage = "This Lab is already assigned"
                return errorMessage
            #there are no existing entry, so we can assign
            assign = labToCourse(labNumber= labNumber, courseNumber=courseNumber)
            assign.save()
        return errorMessage

    def inputValidation(labNumber, courseNumber):
        errorMessage = ""
        # Check for empty inputs
        if len(labNumber) < 1 and len(courseNumber) < 1:
            errorMessage = "No Input Provided!"
            return errorMessage
        elif len(labNumber) < 1:
            errorMessage = "No Lab Number Provided!"
            return errorMessage
        elif len(courseNumber) < 1:
            errorMessage = "No Course Number Provided!"
            return errorMessage

        # Check for too long inputs
        elif len(labNumber) > 3:
            errorMessage = "The Lab Number Is Too Long!"
            return errorMessage

        elif len(courseNumber) > 3:
            errorMessage = "The Course Number Is Too Long!"
            return errorMessage

        # Check for non numeric input
        elif not (labNumber.isnumeric()):
            errorMessage = "The Lab Number Isn't Numeric!"
            return errorMessage
        elif not (courseNumber.isnumeric()):
            errorMessage = "The Course Number Isn't Numeric!"
        return errorMessage

    def retrieveInDatabase(labNumber, courseNumber):
        errorMessage= ""
        lab = myLab.objects.filter(labNumber=labNumber)
        if len(lab) < 1:
            errorMessage = "This Lab Doesn't Exist!"
            return errorMessage

        course = myCourse.objects.filter(courseNumber=courseNumber)
        if len(course) < 1:
            errorMessage = "This Course Doesn't Exist!"
        return errorMessage

