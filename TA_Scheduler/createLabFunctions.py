from .models import myLab


class createLabFunctions:
    def createLab(self, labName):  # self = labNumber
        errorMessage = ""
        if self == "" and labName == "":
            errorMessage = "Lab name and number are empty"
            return errorMessage
        elif self == "":
            errorMessage = "Lab number is empty"
            return errorMessage
        elif labName == "":
            errorMessage = "Lab name is empty"
            return errorMessage

        if len(self) > 10:
            errorMessage = "Lab Number Is Too Long!"
            return errorMessage

        if not (self.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric"
            return errorMessage

        existingLab = list(myLab.objects.filter(labNumber=self))

        if len(existingLab) != 0:
            errorMessage = "Lab Number Already Exists"
            return errorMessage

        if len(labName) > 20:
            errorMessage = "Lab Name Is Too Long!"
            return errorMessage

        errorMessage = ""
        l1 = myLab(labNumber=self, labName=labName)
        l1.save()
        return errorMessage
