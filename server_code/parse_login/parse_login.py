import email_validator

'''
This function takes a string to parse as well as a string to look for. Uses the email_validator
library. Returns the string 'valid' if the email is valid, else returns the error message 
'''

def parse_email(stringToParse, stringToLookFor):
    try:
        #validate the email. Throws an exception
        email = email_validator.validate_email(stringToParse)
        #the email is valid, but it does not match buffalo.edu
        if email.domain is None or email.domain != stringToLookFor:
            return "The email provided does not end in buffalo.edu"
        #return valid otherwise
        return 'valid'   
    except email_validator.EmailNotValidError as e:
        return str(e)
    