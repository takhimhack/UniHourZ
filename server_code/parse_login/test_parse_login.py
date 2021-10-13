import parse_login

regex_str = r"^([^@+]+)+?(\w+)?@([^@]+)"
target_string = "buffalo.edu"

def correctlyIdentify():
    email = "cpneppal@buffalo.edu"
    # parse_login should output true
    return parse_login.parse_login(regex_str, email, target_string)

def incorrectlyIdentify():
    email = "somebody@yahoo.aol.com"
    return not parse_login.parse_login(regex_str, email, target_string)

def garbled_mess():
    email = "asdafas@r2342rwefsdsdfwefsdf"
    return not parse_login.parse_login(regex_str, email, target_string)

def rightendwrongspot():
    email = 'buffalo.edu@aol.com'
    return not parse_login.parse_login(regex_str, email, target_string)

if __name__ == "__main__":
    if not correctlyIdentify():
        print("Testing cpneppal@buffalo.edu should have returned true")
    
    if not incorrectlyIdentify():
        print("Testing somebody@yahoo.aol.com should have returned true")

    if not garbled_mess():
        print("Testing a garbled mess returned true when it shouldn't")

    if not rightendwrongspot():
        print("Testing an email with buffalo.edu as a username yielded a true statement!")
        
