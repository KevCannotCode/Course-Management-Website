from .models import myCourse

class createLabFunctions():
    def createLab(labNumber, labName):
        errorMessage = ""
        if not (labNumber.isnumeric()):
            errorMessage = "Lab Number Isn't Numeric"
        else:
            existingLab = list(myLab.objects.filter(labNumber = labNumber))

            if (len(existingLab) != 0):
                errorMessage = "Course Number Already Exists"
            else:
                errorMessage = ""
                #createCourseFunctions.createCourse1(courseName, courseNumber)
                l1 = myLab(labName= labName, labNumber= labNumber)
                l1.save()
        return errorMessage
        
        
