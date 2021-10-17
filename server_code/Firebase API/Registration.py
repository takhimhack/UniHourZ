from firebaseAPI import *

def registerUser(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        db.child("users")
    except:
        pass

