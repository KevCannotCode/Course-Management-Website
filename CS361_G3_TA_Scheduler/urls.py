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
from TA_Scheduler.views import CreateCourse
from TA_Scheduler.views import CreateLab
from TA_Scheduler.views import Profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login.as_view()),
    path('home/', Home.as_view()),
    path('create-account/', CreateAccount.as_view()),
    path('create-course/', CreateCourse.as_view()),
    path('create-lab/', CreateLab.as_view()),
    path('logout/', Logout.as_view()),
    path('profile/', Profile.as_view())
]
