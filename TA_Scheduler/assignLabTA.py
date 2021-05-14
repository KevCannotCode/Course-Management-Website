from .models import myLabTA
from .models import myLab
from .models import myAccount
from .models import labToCourse
from .models import myCourseInstructor

class assignLabTA:
    def assignLabToTA(labNumber, taUsername, instructorUsername):
        #check the validity of the inputs
        errorMessage = assignLabTA.inputValidation(labNumber, taUsername, instructorUsername)
        #check if the lab and course exist
        if errorMessage == "":
            errorMessage = assignLabTA.retrieveInDatabase(labNumber, taUsername,instructorUsername)
        #check if the instructor is authorized to access this course
        if errorMessage == "":
            errorMessage = assignLabTA.checkInstructor(labNumber, instructorUsername)

        if errorMessage == "":
            #there are no existing entry, so we can assign
            assign = myLabTA(labNumber= labNumber, taUserName= taUsername)
            assign.save()
        return errorMessage

    def inputValidation(labNumber, taUserName, instructorUsername):
        errorMessage = ""
        # Check for empty inputs
        if len(labNumber) < 1 and len(taUserName) < 1:
            errorMessage = "No Input Provided!"
            return errorMessage
        elif len(labNumber) < 1:
            errorMessage = "No Lab Number Provided!"
            return errorMessage
        elif len(taUserName) < 1:
            errorMessage = "No TA Username Provided!"
            return errorMessage
        elif len(instructorUsername) < 1:
            errorMessage = "No Instructor Username Provided!"
            return errorMessage

        # Check for too long inputs
        elif len(labNumber) > 3:
            errorMessage = "The Lab Number Is Too Long!"
            return errorMessage

        elif len(taUserName) > 40:
            errorMessage = "The TA Username Is Too Long!"
            return errorMessage

        elif len(instructorUsername) > 40:
            errorMessage = "The Instructor Username Is Too Long!"
            return errorMessage

        # Check for non numeric input
        elif not (labNumber.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric!"
            return errorMessage
        return errorMessage

    def retrieveInDatabase(labNumber, taUserName, instructorUsername):
        errorMessage = ""
        lab = myLab.objects.filter(labNumber=labNumber)
        if len(lab) < 1:
            errorMessage = "This Lab Doesn't Exist!"
            return errorMessage

        ta = myAccount.objects.filter(userName= taUserName)
        if len(ta) < 1:
            errorMessage = "This TA Doesn't Exist!"
            return errorMessage

        instructor = list(myAccount.objects.filter(userName=instructorUsername))
        if len(instructor) < 1:
            errorMessage = "This Instructor Doesn't Exist!"
            return errorMessage
        # check if there are any existing labToTA entry
        # if a lab is already assigned to a TA, that lab can't be assigned to another TA
        entry = list(myLabTA.objects.filter(labNumber=labNumber))
        if len(entry) != 0:
            errorMessage = "This Lab Already Has A TA!"
            return errorMessage
        return errorMessage

    def checkInstructor(labNumber, instructorUsername):
        errorMessage= ""
        account = list(myAccount.objects.filter(userName= instructorUsername))
        type = account[0].userType
        # checks for the instructor
        # an admin doesn't these checks
        if type != "Administrator":
            entry = list(myCourseInstructor.objects.filter(instructorUserName=instructorUsername))
            if len(entry) < 1:
                errorMessage = "This Instructor Doesn't Have A Course!"
                return errorMessage

            courseNumber = entry[0].courseNumber
            # check if the labNumber and matches this instructor's course
            instructorCourse = list(labToCourse.objects.filter(labNumber= labNumber, courseNumber= courseNumber))
            if len(instructorCourse) < 1:
                errorMessage = "Unauthorized Assignment!"
        return errorMessage
