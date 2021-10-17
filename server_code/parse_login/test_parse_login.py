import parse_login

target_string = "buffalo.edu"

def correctlyIdentify():
    email = "cpneppal@buffalo.edu"
    # parse_email should output true
    return parse_login.parse_email(email, target_string)

def incorrectlyIdentify():
    email = "somebody@yahoo.aol.com"
    return parse_login.parse_email(email, target_string)

def garbled_mess():
    email = "sdfsdfsdfsdfsdfsdse fsadfaer"
    return parse_login.parse_email(email, target_string)

def rightendwrongspot():
    email = 'buffalo.edu@aol.com'
    return parse_login.parse_email(email, target_string)

if __name__ == "__main__":
    print(correctlyIdentify())
    print(incorrectlyIdentify())
    print(garbled_mess())
    print(rightendwrongspot())
