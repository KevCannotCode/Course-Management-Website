from .models import labToCourse
from .models import myLab
from .models import myCourse
class assignLabToCourse:
    def assignLabToCourse(labNumber, courseNumber):
        #check the validity of the inputs
        errorMessage = assignLabToCourse.inputValidation(labNumber, courseNumber)
        #check if the lab and course exist
        errorMessage = assignLabToCourse.retrieveInDatabase(labNumber, courseNumber)

        if errorMessage == "":
            #check if there are any existing labTOcourse entry
            entry = list(labToCourse.objects.filter(labNumber=labNumber, courseNumber=courseNumber) )
            if len(entry) != 0:
                errorMessage = "These lab and course are already assigned"
                return errorMessage
            #there are no existing entry, so we can assign
            assign = labToCourse(labNumber= labNumber, courseNumber=courseNumber)
            assign.save()

        return errorMessage
    def inputValidation(labNumber, courseNumber):
        errorMessage = ""
        # Check for empty inputs
        if len(labNumber) < 1:
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
            errorMessage = "Lab Number Isn't Numeric!"
            return errorMessage
        elif not (courseNumber.isnumeric()):
            errorMessage = "Course Number Isn't Numeric!"
        return errorMessage

    def retrieveInDatabase(labNumber, courseNumber):
        errorMessage= ""
        try:
            lab = myLab.objects.filter(labNumber=labNumber)
        except myLab.DoesNotExist:
            errorMessage = "This Lab Doesn't Exist!"
        try:
            course = myCourse.objects.filter(courseNumber=courseNumber)
        except myCourse.DoesNotExist:
            errorMessage = "This Course Doesnt' Exist"
        finally:
            return errorMessage