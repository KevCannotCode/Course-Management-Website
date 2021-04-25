from .models import myLab


class createLabFunctions:
    def createLab(labNumber, labName):
        errorMessage = ""
        if labNumber == "" and labName == "":
            errorMessage = "Lab name and number are empty"
            return errorMessage
        elif labNumber == "":
            errorMessage = "Lab number is empty"
            return errorMessage
        elif labName == "":
            errorMessage = "Lab name is empty"
            return errorMessage

        if len(labNumber) > 10:
            errorMessage = "Lab Number Is Too Long!"
            return errorMessage

        if not (labNumber.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric"
            return errorMessage

        existingLab = list(myLab.objects.filter(labNumber=labNumber))

        if len(existingLab) != 0:
            errorMessage = "Lab Number Already Exists"
            return errorMessage

        if len(labName) > 20:
            errorMessage = "Lab Name Is Too Long!"
            return errorMessage

        errorMessage = ""
        l1 = myLab(labNumber=labNumber, labName=labName)
        l1.save()
        return errorMessage
