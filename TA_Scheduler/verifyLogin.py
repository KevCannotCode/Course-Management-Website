from django.shortcuts import render
from .models import myAccount
from django.contrib.auth import logout as auth_logout

class verifyLogin():
    def verifyLogin(userName, request):
        userFound = list(myAccount.objects.filter(userName=userName))
        if(len(userFound) == 0):
            auth_logout(request)
            return False
        return True

