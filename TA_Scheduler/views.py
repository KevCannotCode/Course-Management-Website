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

        account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
        lab_list = list(myLab.objects.values_list("labNumber", "labName"))
        contact_list = list(myContact.objects.values_list("userName","phoneNumber", "emailAddress"))

        return render(request, "home.html", {"account_list":account_list, "course_list":course_list, "lab_list":lab_list, "userName":userName, "contact_list":contact_list})


class CreateAccount(View):
    def get(self,request):
        userName = request.session["userName"]
        if(verifyLogin.verifyLogin(userName, request) == False):
            return render(request, "logout.html", {})
        account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
        contact_list = list(myContact.objects.values_list("userName", "phoneNumber", "emailAddress"))
        return render(request,"create-account.html",{"account_list":account_list, "userName":userName, "errorMessage":"", "contact_list":contact_list})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if(verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage = createAccountFunctions.createAccount(request.POST["userName"], request.POST["password"], request.POST["userType"])
            account_list = list(myAccount.objects.values_list("userName", "password", "userType"))
            contact_list = list(myContact.objects.values_list("userName", "phoneNumber", "emailAddress"))
            return render(request,"create-account.html",{"account_list":account_list, "userName":userName, "errorMessage":errorMessage, "contact_list":contact_list})

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
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
        return render(request,"create-course.html",{"course_list":course_list, "userName":userName, "errorMessage":""})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            if (verifyLogin.verifyLogin(userName, request) == False):
                return render(request, "logout.html", {})
            errorMessage = createCourseFunctions.createCourse(request.POST["courseNumber"], request.POST["courseName"])
            course_list = list(myCourse.objects.values_list("courseNumber","courseName"))
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