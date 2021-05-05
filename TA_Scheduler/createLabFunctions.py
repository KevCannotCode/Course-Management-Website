from .models import myLab


class createLabFunctions:
    def createLab(labNumber, labName):
        errorMessage = ""
        if labNumber == "" and labName == "":
            errorMessage = "No Lab Number or Lab Name Provided!"
            return errorMessage
        elif labNumber == "":
            errorMessage = "No Lab Number Provided!"
            return errorMessage
        elif labName == "":
            errorMessage = "No Lab Name Provided!"
            return errorMessage

        if len(labNumber) > 10:
            errorMessage = "Lab Number Is Too Long!"
            return errorMessage

        if not (labNumber.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric!"
            return errorMessage

        existingLab = list(myLab.objects.filter(labNumber=labNumber))

        if len(existingLab) != 0:
            errorMessage = "Lab Number Already Exists!"
            return errorMessage

        if len(labName) > 20:
            errorMessage = "Lab Name Is Too Long!"
            return errorMessage

        errorMessage = ""
        l1 = myLab(labNumber=labNumber, labName=labName, taUserName="NOT SET")
        l1.save()
        return errorMessage
