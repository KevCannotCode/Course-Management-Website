from django.shortcuts import render, redirect
from django.views import View
from .models import myAccount
from .models import myCourse
from .models import myLab
from .models import myContact
from .createCourseFunctions import createCourseFunctions
from .createLabFunctions import createLabFunctions
from .createAccount import createAccountFunctions
from .myLogin import myLogin
from django.contrib.auth import logout as auth_logout
from .verifyLogin import verifyLogin
from .models import myCourseInstructor
from .models import myLabTA

# Create your views here.
class Login(View):
    def get(self,request):
        try:
            userName = request.session["userName"]
            return redirect("/home/")
            print("userName: " + userName)
        except:
            pass
        return render(request,"index.html",{})

    def post(self,request):
        if len(request.POST) != 0:
            errorMessage = myLogin.login(request.POST['userName'], request.POST['password'])
            if(errorMessage != ""):
                return render(request, "index.html", {"errorMessage": errorMessage})
            else:
                m = myAccount.objects.get(userName=request.POST['userName'])
                request.session["userName"] = m.userName
                request.session["userType"] = m.userType
                request.session["error"] = ""


                return redirect("/home/")

class Logout(View):
    def get(self,request):
        auth_logout(request)
        return render(request,"logout.html",{})

class Home(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})



        #errorMessage=""
        #errorMessage=request.session["error"]
        #request.session["error"] = ""

        account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName", "instructorUserName"))
        lab_list = list(myLab.objects.values_list("labNumber", "labName"))
        contact_list = list(myContact.objects.values_list("userName","phoneNumber", "emailAddress"))

        if(request.session["userType"] == "Administrator"):
            return render(request, "home.html", {"account_list":account_list, "course_list":course_list, "lab_list":lab_list, "userName":userName, "contact_list":contact_list, "errorMessage":""})
        elif(request.session["userType"] == "Instructor"):
            return render(request, "home-instructor.html", {"account_list":account_list, "course_list":course_list, "lab_list":lab_list, "userName":userName, "contact_list":contact_list, "errorMessage":""})




class CreateAccount(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})
        account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
        contact_list = list(myContact.objects.values_list("userName", "phoneNumber", "emailAddress"))
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName", "instructorUserName"))
        return render(request,"create-account.html",{"course_list":course_list, "account_list":account_list, "userName":userName, "errorMessage":"", "contact_list":contact_list})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage = createAccountFunctions.createAccount(request.POST["userName"], request.POST["password"], request.POST["userType"])
            account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
            contact_list = list(myContact.objects.values_list("userName", "phoneNumber", "emailAddress"))
            course_list = list(myCourse.objects.values_list("courseNumber", "courseName", "instructorUserName"))
            return render(request,"create-account.html",{"course_list":course_list, "account_list":account_list, "userName":userName, "errorMessage":errorMessage, "contact_list":contact_list})

class DeleteAccount(View):
    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})



            deleteAccount = list(myAccount.objects.filter(userName=request.POST["deleteAccount"]))[0]
            deleteAccount.delete()
            deleteContact = list(myContact.objects.filter(userName=request.POST["deleteAccount"]))[0]
            deleteContact.delete()
            return redirect(request.POST["returnUrl"])

class CreateCourse(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName", "instructorUserName"))
        return render(request,"create-course.html",{"course_list":course_list, "userName":userName, "errorMessage":""})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if (verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage = createCourseFunctions.createCourse(request.POST["courseNumber"], request.POST["courseName"])
            course_list = list(myCourse.objects.values_list("courseNumber","courseName", "instructorUserName"))
            return render(request,"create-course.html", {"course_list":course_list, "errorMessage":errorMessage, "userName":userName})

class DeleteCourse(View):
    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})

            deleteCourse = list(myCourse.objects.filter(courseNumber=request.POST["deleteCourse"]))[0]
            deleteCourse.delete()

            return redirect(request.POST["returnUrl"])

class CreateLab(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})
        lab_list = list(myLab.objects.values_list("labNumber", "labName"))
        return render(request,"create-lab.html",{"lab_list":lab_list, "userName":userName, "errorMessage":""})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if (verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage = createLabFunctions.createLab(request.POST["labNumber"], request.POST["labName"])
            lab_list = list(myLab.objects.values_list("labNumber","labName"))
            return render(request,"create-lab.html", {"lab_list":lab_list, "errorMessage":errorMessage, "userName":userName})

class DeleteLab(View):
    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})

            deleteLab = list(myLab.objects.filter(labNumber=request.POST["deleteLab"]))[0]
            deleteLab.delete()
            return redirect(request.POST["returnUrl"])

class Profile(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})

        contact = list(myContact.objects.filter(userName=userName))[0]
        return render(request, "profile.html", {"userName":userName, "phoneNumber":contact.phoneNumber, "emailAddress":contact.emailAddress})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})

            contact = list(myContact.objects.filter(userName=userName))[0]
            contact.phoneNumber = request.POST["phoneNumber"]
            contact.emailAddress = request.POST["emailAddress"]
            contact.save()
            return render(request, "profile.html", {"userName":userName, "phoneNumber":contact.phoneNumber, "emailAddress":contact.emailAddress})


class AssignCourseInstructor(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})


        errorMessage=request.session["error"]
        request.session["error"] = ""

        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
        account_list = list(myAccount.objects.values_list("userName", "userType"))
        assigned_course_list = list(myCourseInstructor.objects.values_list("courseNumber", "instructorUserName"))
        return render(request,"assign-course-instructor.html",{"assigned_course_list":assigned_course_list, "course_list":course_list, "account_list":account_list, "userName":userName, "errorMessage":errorMessage})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if (verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})

            errorMessage = ""

            courseNumber = request.POST["courseNumber"]
            if not(courseNumber.isnumeric()):
                errorMessage="Invalid Course Number!"
            else:
                existingCourseInstructor = list(
                myCourseInstructor.objects.filter(courseNumber=request.POST["courseNumber"]))
                existingCourse = list(myCourse.objects.filter(courseNumber=courseNumber))
                existingInstructor = list(
                myAccount.objects.filter(userName=request.POST["instructorUserName"], userType="Instructor"))
                if((len(existingCourse) == 0) and (len(existingInstructor) == 0)):
                    errorMessage="Invalid Course Number And Instructor Username!"
                elif((len(existingCourse) == 0)):
                    errorMessage="Invalid Course Number!"
                elif((len(existingInstructor) == 0)):
                    errorMessage="Invalid Instructor Username!"
                elif ((len(existingCourseInstructor) != 0)):
                    errorMessage="This Course Already Has An Instructor!"
            if(errorMessage is not ""):
                course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
                account_list = list(myAccount.objects.values_list("userName", "userType"))
                assigned_course_list = list(myCourseInstructor.objects.values_list("courseNumber", "instructorUserName"))

                return render(request, "assign-course-instructor.html", {"assigned_course_list": assigned_course_list, "course_list": course_list, "account_list": account_list, "errorMessage": errorMessage, "userName": userName})


            newAssignment = myCourseInstructor(courseNumber=request.POST["courseNumber"], instructorUserName=request.POST["instructorUserName"])
            newAssignment.save()

            course = list(myCourse.objects.filter(courseNumber=request.POST["courseNumber"]))[0]
            course.instructorUserName = request.POST["instructorUserName"]
            course.save()

            course_list = list(myCourse.objects.values_list("courseNumber","courseName"))
            account_list = list(myAccount.objects.values_list("userName", "userType"))
            assigned_course_list = list(myCourseInstructor.objects.values_list("courseNumber", "instructorUserName"))

            return render(request,"assign-course-instructor.html", {"assigned_course_list":assigned_course_list, "course_list":course_list, "account_list":account_list, "errorMessage":errorMessage, "userName":userName})

class DeleteCourseInstructor(View):
    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage=""
            #deleteCourseInstructor = list(myCourseInstructor.objects.filter(courseNumber=request.POST["deleteCourseInstructor"]))[0]
            deleteCourseInstructor = list(myCourseInstructor.objects.filter(courseNumber=request.POST["deleteCourseInstructor"]))
            if(len(deleteCourseInstructor) != 0):
                deleteCourseInstructor[0].delete()
            else:
                errorMessage="Course Assignment Not Found!"

            course = list(myCourse.objects.filter(courseNumber=request.POST["deleteCourseInstructor"]))[0]
            course.instructorUserName = "NOT SET"
            course.save()

            request.session["error"] = errorMessage
            return redirect(request.POST["returnUrl"])




class AssignLabTa(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})


        errorMessage=request.session["error"]
        request.session["error"] = ""

        lab_list = list(myLab.objects.values_list("labNumber", "labName"))
        account_list = list(myAccount.objects.values_list("userName", "userType"))
        assigned_lab_list = list(myLabTA.objects.values_list("labNumber", "taUserName"))
        return render(request,"assign-lab-ta.html",{"assigned_lab_list":assigned_lab_list, "lab_list":lab_list, "account_list":account_list, "userName":userName, "errorMessage":errorMessage})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if (verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})

            errorMessage = ""

            labNumber = request.POST["labNumber"]
            if not(labNumber.isnumeric()):
                errorMessage="Invalid Lab Number!"
            else:
                existingLabTa = list(myLabTA.objects.filter(labNumber=request.POST["labNumber"]))
                existingLab = list(myLab.objects.filter(labNumber=labNumber))
                existingTa = list(myAccount.objects.filter(userName=request.POST["taUserName"], userType="TA"))
                if((len(existingLab) == 0) and (len(existingLab) == 0)):
                    errorMessage="Invalid Lab Number And TA Username!"
                elif((len(existingLab) == 0)):
                    errorMessage="Invalid Lab Number!"
                elif((len(existingTa) == 0)):
                    errorMessage="Invalid TA Username!"
                elif ((len(existingLabTa) != 0)):
                    errorMessage="This Lab Already Has A TA!"
            if(errorMessage is not ""):
                lab_list = list(myLab.objects.values_list("labNumber", "labName"))
                account_list = list(myAccount.objects.values_list("userName", "userType"))
                assigned_lab_list = list(myLabTA.objects.values_list("labNumber", "taUserName"))

                return render(request, "assign-lab-ta.html", {"assigned_lab_list": assigned_lab_list, "lab_list": lab_list, "account_list": account_list, "errorMessage": errorMessage, "userName": userName})


            newAssignment = myLabTA(labNumber=request.POST["labNumber"], taUserName=request.POST["taUserName"])
            newAssignment.save()

            lab = list(myLab.objects.filter(labNumber=request.POST["labNumber"]))[0]
            lab.instructorUserName = request.POST["taUserName"]
            lab.save()

            lab_list = list(myLab.objects.values_list("labNumber", "labName"))
            account_list = list(myAccount.objects.values_list("userName", "userType"))
            assigned_lab_list = list(myLabTA.objects.values_list("labNumber", "taUserName"))

            return render(request,"assign-lab-ta.html", {"assigned_lab_list":assigned_lab_list, "lab_list":lab_list, "account_list":account_list, "errorMessage":errorMessage, "userName":userName})

class DeleteLabTa(View):
    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage=""
            deleteLabTa = list(myLabTA.objects.filter(labNumber=request.POST["deleteLabTa"]))
            if(len(deleteLabTa) != 0):
                deleteLabTa[0].delete()
            else:
                errorMessage="Lab Assignment Not Found!"

            lab = list(myLab.objects.filter(labNumber=request.POST["deleteLabTa"]))[0]
            lab.instructorUserName = "NOT SET"
            lab.save()

            request.session["error"] = errorMessage
            return redirect(request.POST["returnUrl"])