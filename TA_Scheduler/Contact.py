from .models import myContact
from .models import myAccount
class Contact:
    def createContact(phoneNumber, email):

        errorMessage = ""
        #check if empty info
        if phoneNumber == "" and email == "":
            errorMessage = "No Phone Number or email Provided!"
            return errorMessage
        elif phoneNumber == "":
            errorMessage = "No Phone Number Provided!"
            return errorMessage
        elif email == "":
            errorMessage = "No email Provided!"
            return errorMessage



        # check if the phone number is valid
        if not (phoneNumber.isnumeric()):
            errorMessage = "The phone number Isn't Numeric. Invalid Phone number format"
            return errorMessage

        else:
            if (len(phoneNumber) != 10):
                errorMessage = "The phone number entered isn't 10 digits long. Invalid Phone number format"
                return errorMessage
            # what exactly do I create a list?
            existingPhoneNumber = list(myContact.objects.filter(phoneNumber=phoneNumber))

            if (len(existingPhoneNumber) != 0):
                errorMessage = "Phone number belongs to another account. Duplicate error"
                return errorMessage

            existingEmail = list(myContact.objects.filter(emailAddress=email))

            if (len(existingEmail) != 0):
                errorMessage = "Email belongs to another account. Duplicate error"
                return errorMessage


        # check the validity of the email
            if (email._contains_('@')):
                if(email._contains_('.com') or email._contains_('.edu') or email._contains_('.org')):
                    emailarray1 = email.split('@')
                    emailarray2 = emailarray1[1].split('.')
                    if(bool(emailarray1[0].match('^[a-zA-Z0-9]*$')) or bool(emailarray2[0].match('^[a-zA-Z0-9]*$'))):
                        errorMessage = "Email cannot have special characters. Invalid email format"
                        return errorMessage
                    else:
                        if (emailarray2[1] != '.com' or emailarray2[1] != '.edu' or emailarray2[1] != '.org'):
                            errorMessage = "Email suffix must be ONLY .com, .edu, or .org. Invalid email format"
                            return errorMessage




                else:
                    errorMessage = "Email requires one of .com,.edu, or .org. Invalid email format"
                    return errorMessage
            else:
                errorMessage = "Email requires @ .Invalid email format"
                return errorMessage

        c1 = myContact(userName=myAccount.userName, phoneNumber=phoneNumber, email=email)
        c1.save()
        return errorMessage


    def setPhoneNumber(setNumber):
        errorMessage=''
        if not (setNumber.isnumeric()):
            errorMessage = "The phone number Isn't Numeric. Invalid Phone number format"
            return errorMessage

        else:
            if (len(setNumber) != 10):
                errorMessage = "The phone number entered isn't 10 digits long. Invalid Phone number format"
                return errorMessage
            # what exactly do I create a list?
            existingPhoneNumber = list(myContact.objects.filter(phoneNumber=setNumber))

            if (len(existingPhoneNumber) != 0):
                errorMessage = "Phone number belongs to another account. Duplicate error"
                return errorMessage
        myContact.phoneNumber = setNumber
        return errorMessage


    def setEmail(setEmail):
        errorMessage=''
        existingEmail = list(myContact.objects.filter(emailAddress=setEmail))

        if (len(existingEmail) != 0):
            errorMessage = "Email belongs to another account. Duplicate error"
            return errorMessage

        # check the validity of the email
        if (setEmail._contains_('@')):
            if (setEmail._contains_('.com') or setEmail._contains_('.edu') or setEmail._contains_('.org')):
                emailarray1 = setEmail.split('@')
                emailarray2 = emailarray1[1].split('.')
                if (bool(emailarray1[0].match('^[a-zA-Z0-9]*$')) or bool(emailarray2[0].match('^[a-zA-Z0-9]*$'))):
                    errorMessage = "Email cannot have special characters. Invalid email format"
                    return errorMessage
                else:
                    if (emailarray2[1] != '.com' or emailarray2[1] != '.edu' or emailarray2[1] != '.org'):
                        errorMessage = "Email suffix must be ONLY .com, .edu, or .org. Invalid email format"
                        return errorMessage



            else:
                errorMessage = "Email requires one of .com,.edu, or .org. Invalid email format"
                return errorMessage
        else:
            errorMessage = "Email requires @ .Invalid email format"
            return errorMessage


        myContact.emailAddress = setEmail
        return errorMessage
