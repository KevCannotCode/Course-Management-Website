from .models import labToCourse

class labToCourse:
    def assignLabToCourse(labNumber, courseNumber):
        errorMessage = ""
        try:
            #Check for empty inputs
            if len(labNumber) < 1:
                errorMessage = "No Lab Number Provided!"
                return errorMessage
            elif len(courseNumber) < 1:
                errorMessage = "No Course Number Provided!"
                return errorMessage

            # Check for too long inputs
            elif len(labNumber) > 3:
                errorMessage = "The Lab Number Is Too Long!"
                return errorMessage

            elif len(courseNumber) > 3:
                errorMessage = "The Course Number Is Too Long!"
                return errorMessage

            #Check for non numeric input
            elif not (labNumber.isnumeric() ):
                errorMessage = "Lab Number Isn't Numeric!"
                return errorMessage
            elif not (labNumber.isnumeric()):
                errorMessage = "Lab Number Isn't Numeric!"
            return errorMessage

        return errorMessage