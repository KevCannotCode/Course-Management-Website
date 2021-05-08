"""CS361_G3_TA_Scheduler URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TA_Scheduler.views import Login
from TA_Scheduler.views import Logout
from TA_Scheduler.views import Home
from TA_Scheduler.views import CreateAccount
from TA_Scheduler.views import DeleteAccount
from TA_Scheduler.views import CreateCourse
from TA_Scheduler.views import DeleteCourse
from TA_Scheduler.views import CreateLab
from TA_Scheduler.views import DeleteLab
from TA_Scheduler.views import Profile
from TA_Scheduler.views import AssignCourseInstructor
from TA_Scheduler.views import DeleteCourseInstructor
from TA_Scheduler.views import AssignLabTa
from TA_Scheduler.views import DeleteLabTa
from TA_Scheduler.views import AssignCourseLab
from TA_Scheduler.views import DeleteCourseLab


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login.as_view()),
    path('home/', Home.as_view()),
    path('create-account/', CreateAccount.as_view()),
    path('delete-account/', DeleteAccount.as_view()),
    path('create-course/', CreateCourse.as_view()),
    path('delete-course/', DeleteCourse.as_view()),
    path('create-lab/', CreateLab.as_view()),
    path('delete-lab/', DeleteLab.as_view()),
    path('logout/', Logout.as_view()),
    path('profile/', Profile.as_view()),
    path('assign-course-instructor/', AssignCourseInstructor.as_view()),
    path('delete-course-instructor/', DeleteCourseInstructor.as_view()),
    path('assign-lab-ta/', AssignLabTa.as_view()),
    path('delete-lab-ta/', DeleteLabTa.as_view()),
    path('assign-course-lab/', AssignCourseLab.as_view()),
    path('delete-course-lab/', DeleteCourseLab.as_view())

]
