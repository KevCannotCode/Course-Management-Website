from .models import myCourse

class createCourseFunctions():
    def createCourse(courseNumber, courseName):
        errorMessage = ""
        if not (courseNumber.isnumeric()):
            errorMessage = "Course Number Isn't Numeric"
        else:
            existingCourse = list(myCourse.objects.filter(courseNumber=courseNumber))

            if (len(existingCourse) != 0):
                errorMessage = "Course Number Already Exists"
            else:
                errorMessage = ""
                #createCourseFunctions.createCourse1(courseName, courseNumber)
                c1 = myCourse(courseName=courseName, courseNumber=courseNumber)
                c1.save()
        return errorMessage