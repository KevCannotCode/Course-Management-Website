from .models import myCourse

class createCourseFunctions():
    def createCourse(courseNumber, courseName):
        errorMessage = ""
        if(courseNumber == ""):
            if(courseName == ""):
                errorMessage = "No Course Number or Course Name Provided!"
                return errorMessage
            errorMessage = "No Course Number Provided!"
            return errorMessage
        if (courseName == ""):
            errorMessage = "No Course Name Provided!"
            return errorMessage
        if not (courseNumber.isnumeric()):
            errorMessage = "Course Number Isn't Numeric"
            return errorMessage
        else:
            existingCourse = list(myCourse.objects.filter(courseNumber=courseNumber))

            if (len(existingCourse) != 0):
                errorMessage = "Course Number Already Exists"
                return errorMessage
            else:
                #createCourseFunctions.createCourse1(courseName, courseNumber)
                c1 = myCourse(courseName=courseName, courseNumber=courseNumber)
                c1.save()
                errorMessage = ""
                return errorMessage