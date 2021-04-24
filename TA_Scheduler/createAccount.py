from .models import myAccount

class createAccountFunctions():
    def createAccount(username, password):
        errorMessage = ""

        #check size of inputted username and password
        if len(username) < 1 or len(username) > 40:
            errorMessage = "Invalid username"
        elif len(password) < 1 or len(password) > 40:
            errorMessage = "Invalid password"
        else:
            existingAccounts = list(myCourse.objects.filter(username=username))

        #check database to see if there is an account that already exists
        if (len(existingAccounts) != 0):
            errorMessage = "An account with this username already exits"
        else:
            #creates new account with inputted fields and saves it to the database
            newAccount = myAccount(username, password)
            nexAccount.save()

        return errorMessage