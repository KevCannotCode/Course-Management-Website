from .models import myAccount

class Login():
    def login(self, username, password):
        # query the username as a pk
        errorMessage = ""
        try:
            #checking for long inputs
            if len(username) > 40:
                errorMessage = "The username is too short"
            if len(password) > 40 :
                errorMessage = "The password is too long"
            #checking for empty inputs
            if len(username) < 1:
                errorMessage = "The username empty"
            if len(password) < 1:
                errorMessage = "The password is empty"
            #check if the username is non existant
            entry = myAccount.objects.get(username = username)
            #check if the password matches the username
            if( entry.password is not password):
                errorMessage = "The password does not match this username"
        #do you think i SHould check for the type?
        except myAccount.DoesNotExist:
            errorMessage = "The username was not found in the database"
        except myAccount.MultipleObjectsReturned:
            errorMessage = "There was a duplicate of the username in the database"
        finally:
            return errorMessage
