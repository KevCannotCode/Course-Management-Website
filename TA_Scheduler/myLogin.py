from .models import myAccount


class myLogin():
    def login(username, password):
        # query the username as a pk
        errorMessage = ""
        try:
            # checking for long inputs
            if len(username) > 40:
                errorMessage = "The username is too long"
                return errorMessage
            elif len(password) > 40:
                errorMessage = "The password is too long"
                return errorMessage
            # checking for empty inputs
            elif len(username) < 1:
                errorMessage = "The username is empty"
                return errorMessage
            elif len(password) < 1:
                errorMessage = "The password is empty"
                return errorMessage
            # check if the username is non existant
            if errorMessage != "":
                entry = myAccount.objects.get(userName=username)
            # check if the password matches the username
                if (entry.password != password):
                    errorMessage = "The password does not match this username"

        except myAccount.DoesNotExist:
            errorMessage = "The username was not found in the database"
        except myAccount.MultipleObjectsReturned:
            errorMessage = "There was a duplicate of the username in the database"
        finally:
            return errorMessage
