from server_code.FirebaseAPI.firebaseAPI import *

def registerUser(decoded_response):
    try:
        user = auth.create_user_with_email_and_password(decoded_response['email'], decoded_response['password'])
        data_storage = {
            decoded_response['name']: {
                'name': decoded_response['name'],
                'email': decoded_response['email'],
                'typeofUser': decoded_response['typeofUser']
            }
        }
        db.child('users').set(data_storage, user['idToken'])
        return "valid"
        
    except Exception as e:
        return "error has been found!" + str(e)
