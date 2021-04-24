from .models import myContact

class Contact():
    def createContact(phoneNumber, email):
        errorMessage = ""
        existingContact = ()

        #check if the phone number is valid
        if not (phoneNumber.isnumeric()):
            errorMessage = "The phone number Isn't Numeric"

        else:
            #what exactly do I create a list?
            existingContact = list(myContact.objects.filter(phoneNumber = phoneNumber) )

        if (len(existingContact) != 0):
                errorMessage = "Phone Number Already Exists"
        #check the validity of the email
        if()
            else:
                #createCourseFunctions.createCourse1(courseName, courseNumber)
                c = myContact(phoneNumber= phoneNumber, email = email)
                c1.save()
        return errorMessage