from .models import myAccount

class createAccountFunctions():
    def createAccount(userName, password):
        errorMessage = ""

        #check size of inputted username and password
        if userName == "":
            errorMessage = "Blank userName"
            return errorMessage
        elif len(userName) > 40:
            errorMessage = "UserName too long"
            return errorMessage
        elif password == "":
            errorMessage = "Blank password"
            return errorMessage
        elif len(password) > 40:
            errorMessage = "Paswword too long"
            return errorMessage
        else:
            existingAccounts = list(myAccount.objects.filter(userName=userName))

        #check database to see if there is an account that already exists
        if (len(existingAccounts) != 0):
            errorMessage = "An account with this userName already exits"
        else:
            #creates new account with inputted fields and saves it to the database
            newAccount = myAccount(userName, password)
            newAccount.save()

        return errorMessage
