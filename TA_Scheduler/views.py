from django.shortcuts import render, redirect
from django.views import View
from .models import myAccount
from .models import myCourse
from .createCourseFunctions import createCourseFunctions

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,"index.html",{})
    def post(self,request):
        noSuchUser = False
        badPassword = False
        if(request.POST['userName'] == ""):
            return render(request, "index.html", {"message": "bad password"})
        try:
            m = myAccount.objects.get(userName=request.POST['userName'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "index.html", {"message": "User doesn't exist"})
        elif badPassword:
            return render(request,"index.html",{"message":"bad password"})
        else:
            request.session["userName"] = m.userName
            return redirect("/home/")

class Home(View):
    def get(self,request):
        userName = request.session["userName"]

        account_list = list(myAccount.objects.values_list("userName", "password"))
        course_list = list(myCourse.objects.values_list("courseNumber", "courseName"))

        return render(request, "home.html", {"account_list":account_list, "course_list":course_list, "userName":userName})


class CreateAccount(View):
    def get(self,request):
        return render(request,"create-account.html",{})


class CreateCourse(View):
    def get(self,request):
        return render(request,"create-course.html",{})

    def post(self,request):
        if len(request.POST) != 0:

            errorMessage = createCourseFunctions.createCourse(request.POST["courseNumber"], request.POST["courseName"])
            course_list = list(myCourse.objects.values_list("courseNumber","courseName"))
            return render(request,"create-course.html", {"course_list":course_list, "errorMessage":errorMessage})


class CreateLab(View):
    def get(self,request):
        return render(request,"create-lab.html",{})