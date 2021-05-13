
from .models import myCourseInstructor
from .models import myCourse
from .models import myAccount

class assignCourseInstructor:
    def assignCourseInstructor(courseNumber, instructorUserName):
        errorMessage = ""
        if not (courseNumber.isnumeric()):
            errorMessage = "Invalid Course Number!"
        else:
            existingCourseInstructor = list(myCourseInstructor.objects.filter(courseNumber=courseNumber))
            existingCourse = list(myCourse.objects.filter(courseNumber=courseNumber))
            existingInstructor = list(
                myAccount.objects.filter(userName=instructorUserName, userType="Instructor"))
            if ((len(existingCourse) == 0) and (len(existingInstructor) == 0)):
                errorMessage = "Invalid Course Number And Instructor Username!"
            elif ((len(existingCourse) == 0)):
                errorMessage = "Invalid Course Number!"
            elif ((len(existingInstructor) == 0)):
                errorMessage = "Invalid Instructor Username!"
            elif ((len(existingCourseInstructor) != 0)):
                errorMessage = "This Course Already Has An Instructor!"
        if (errorMessage != ""):
            return errorMessage
        else:
            newAssignment = myCourseInstructor(courseNumber=courseNumber,instructorUserName=instructorUserName)
            newAssignment.save()

            course = list(myCourse.objects.filter(courseNumber=courseNumber))[0]
            course.instructorUserName = instructorUserName
            course.save()
            return errorMessage