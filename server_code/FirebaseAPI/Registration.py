from server_code.FirebaseAPI.firebaseAPI import *

def registerUser(decoded_response):
    try:
        auth.create_user_with_email_and_password(decoded_response['email'], decoded_response['password'])
        data_storage = {
                'name': decoded_response['name'],
                'email': decoded_response['email'],
                'typeofUser': decoded_response['typeofUser']
        }
        server_db.child('users').child(decoded_response['name']).set(data_storage)
        return "valid"
        
    except Exception as e:
        return "error has been found!" + str(e)

