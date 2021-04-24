from .models import myAccount

class createAccountFunctions():
    def createAccount(userName, password):
        errorMessage = ""

        #check size of inputted username and password
        if (len(userName) < 1 or len(userName) > 40) or (len(password) < 1 or len(password) > 40):
            errorMessage = "Invalid userName and/or password"
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