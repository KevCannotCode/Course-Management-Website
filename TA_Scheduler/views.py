from django.shortcuts import render, redirect
from django.views import View
from .models import myAccount
from .models import myCourse
from .models import myLab
from .models import myContact
from .createCourseFunctions import createCourseFunctions
from .myLogin import myLogin
from django.contrib.auth import logout as auth_logout

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

        account_list = list(myAccount.objects.values_list("userName", "password"))
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
        lab_list = list(myLab.objects.values_list("labNumber", "labName"))

        return render(request, "home.html", {"account_list":account_list, "course_list":course_list, "lab_list":lab_list, "userName":userName})


class CreateAccount(View):
    def get(self,request):
        userName = request.session["userName"]
        account_list = list(myAccount.objects.values_list("userName", "password"))
        return render(request,"create-account.html",{"account_list":account_list, "userName":userName})


class CreateCourse(View):
    def get(self,request):
        userName = request.session["userName"]
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))
        return render(request,"create-course.html",{"course_list":course_list, "userName":userName, "errorMessage":""})

    def post(self,request):
        if len(request.POST) != 0:
            userName = request.session["userName"]
            errorMessage = createCourseFunctions.createCourse(request.POST["courseNumber"], request.POST["courseName"])
            course_list = list(myCourse.objects.values_list("courseNumber","courseName"))
            return render(request,"create-course.html", {"course_list":course_list, "errorMessage":errorMessage, "userName":userName})


class CreateLab(View):
    def get(self,request):
        userName = request.session["userName"]
        lab_list = list(myLab.objects.values_list("labNumber", "labName"))
        return render(request,"create-lab.html",{"lab_list":lab_list, "userName":userName})


class Profile(View):
    def get(self,request):
        userName = request.session["userName"]

        if(len(list(myContact.objects.filter(userName=userName))) == 0):
            myContact.objects.create(userName=userName, phoneNumber="NOT SET", emailAddress="NOT SET")

        contact = list(myContact.objects.filter(userName=userName))[0]
        return render(request, "profile.html", {"userName":userName, "phoneNumber":contact.phoneNumber, "emailAddress":contact.emailAddress})

    def post(self,request):
        userName = request.session["userName"]

        if(len(list(myContact.objects.filter(userName=userName))) == 0):
            myContact.objects.create(userName=userName, phoneNumber="NOT SET", emailAddress="NOT SET")

        contact = list(myContact.objects.filter(userName=userName))[0]
        contact.phoneNumber = request.POST["phoneNumber"]
        contact.emailAddress = request.POST["emailAddress"]
        contact.save()
        return render(request, "profile.html", {"userName":userName, "phoneNumber":contact.phoneNumber, "emailAddress":contact.emailAddress})