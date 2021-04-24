from .models import myAccount

class Login():
    def login(self, username, password):
        # query the username as a pk
        logged = True
        try:
            entry = myAccount.objects.get(username = username)
            if( entry.password is not password):
                logged = False
        except myAccount.DoesNotExist:
            logged = False
        except myAccount.MultipleObjectsReturned:
            logged = False
        finally:
            return logged