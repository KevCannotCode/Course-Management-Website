from .models import myAccount
from .models import myContact

class createAccountFunctions():
    def createAccount(userName, password, userType):
        errorMessage = ""
        print(userType)
        #check size of inputted username and password
        if userName == "" and password == "":
            errorMessage = "No Username or Password Provided!"
            return errorMessage
        if userName == "":
            errorMessage = "No Username Provided!"
            return errorMessage
        elif len(userName) > 40:
            errorMessage = "UserName Is Too Long!"
            return errorMessage
        elif password == "":
            errorMessage = "No Password Provided!"
            return errorMessage
        elif len(password) > 40:
            errorMessage = "Password Is Too Long!"
            return errorMessage
        elif(not(userType == "Administrator" or userType == "Instructor" or userType == "TA")):
            errorMessage = "Choose A Valid User Type!"
            return errorMessage
        else:
            existingAccounts = list(myAccount.objects.filter(userName=userName))

        #check database to see if there is an account that already exists
        if (len(existingAccounts) != 0):
            errorMessage = "Username Already Exists!"
            return errorMessage


        else:
            #creates new account with inputted fields and saves it to the database
            newAccount = myAccount(userName=userName, password=password, userType=userType)
            newAccount.save()
            newContact = myContact(userName=userName, phoneNumber="NOT SET", emailAddress="NOT SET")
            newContact.save()

        return errorMessage
