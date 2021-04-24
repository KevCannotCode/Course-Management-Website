from .models import myAccount


class myLogin():
    def login(username, password):
        # query the username as a pk
        errorMessage = ""
        try:
            # checking for long inputs
            if len(username) > 40:
                errorMessage = "The Username Is Too Long!"
                return errorMessage
            elif len(password) > 40:
                errorMessage = "The Password Is Too Long!"
                return errorMessage
            # checking for empty inputs
            elif len(username) < 1:
                errorMessage = "No Username Provided!"
                return errorMessage
            elif len(password) < 1:
                errorMessage = "No Password Provided!"
                return errorMessage
            # check if the username is non existant
            if errorMessage == "":
                entry = myAccount.objects.get(userName=username)
            # check if the password matches the username
                if entry.password != password:
                    errorMessage = "Incorrect Password!"

        except myAccount.DoesNotExist:
            errorMessage = "User doesn't exist"
        except myAccount.MultipleObjectsReturned:
            errorMessage = "Duplicate User Found In Database!"
        finally:
            return errorMessage
