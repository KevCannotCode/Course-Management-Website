from .models import myLabTA
from .models import myLab
from .models import myAccount

class assignLabTA:
    def assignLabToTA(labNumber, taUsername):
        #check the validity of the inputs
        errorMessage = assignLabTA.inputValidation(labNumber, taUsername)
        #check if the lab and course exist
        errorMessage = assignLabTA.retrieveInDatabase(labNumber, taUsername)

        if errorMessage == "":
            #check if there are any existing labToTA entry
            #if a lab is already assigned to a TA, that lab can't be assigned to another TA
            entry = list(assignLabTA.objects.filter(labNumber=labNumber))
            if len(entry) != 0:
                errorMessage = "This Lab already has a TA"
                return errorMessage
            #there are no existing entry, so we can assign
            assign = assignLabTA(labNumber= labNumber, taUserName= taUsername)
            assign.save()
        return errorMessage

    def inputValidation(labNumber, taUserName):
        errorMessage = ""
        # Check for empty inputs
        if len(labNumber) < 1:
            errorMessage = "No Lab Number Provided!"
            return errorMessage
        elif len(taUserName) < 1:
            errorMessage = "No TA Username Provided!"
            return errorMessage

        # Check for too long inputs
        elif len(labNumber) > 3:
            errorMessage = "The Lab Number Is Too Long!"
            return errorMessage

        elif len(taUserName) > 40:
            errorMessage = "The TA Username Is Too Long!"
            return errorMessage

        # Check for non numeric input
        elif not (labNumber.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric!"
            return errorMessage

    def retrieveInDatabase(labNumber, taUserName):
        errorMessage= ""
        try:
            lab = myLab.objects.filter(labNumber=labNumber)
        except myLab.DoesNotExist:
            errorMessage = "This Lab Doesn't Exist!"
        try:
            course = myAccount.objects.filter(username=taUserName)
        except myAccount.DoesNotExist:
            errorMessage = "This TA Doesnt' Exist"
        finally:
            return errorMessage