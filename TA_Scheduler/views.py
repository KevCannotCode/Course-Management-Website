from django.shortcuts import render
from django.views import View
from .models import myAccount
# Create your views here.
class Home(View):
    def get(self,request):
        return render(request,"index.html",{})
    def get(self,request):
        account_list = list(myAccount.objects.values_list("firstName","lastName","userName","email","phone","userType"))
        return render(request, "index.html", {"account_list":account_list})
