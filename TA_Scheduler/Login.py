from .models import myAccount

class Login():
    def login(self, username, password):
        # query the username as a pk
        errorMessage = ""
        try:
            entry = myAccount.objects.get(username = username)
            if( entry.password is not password):
                logged = False
        except myAccount.DoesNotExist:
            errorMessage = "The username was not found in the database"
        except myAccount.MultipleObjectsReturned:
            errorMessage = "There was a duplicate of the username in the database"
        finally:
            return errorMessage