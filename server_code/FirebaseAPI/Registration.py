from server_code.FirebaseAPI.firebaseAPI import *

def registerUser(decoded_response):
    try:
        user = auth.create_user_with_email_and_password(decoded_response['email'], decoded_response['password'])
        if decoded_response['typeofUser'] == 'Student':
            registerStudent(user['localId'], decoded_response)      
        elif decoded_response['typeofUser'] == 'Instructor':
            registerInstructor(user['localId'], decoded_response)
        return "valid"
        
    except Exception as e:
        print("error has been found!" + str(e))

def registerStudent(uid: str, decoded_response):
    #put the student in the "students" section in firebase
    studentInformation = {
        'name': decoded_response['name'],
        'email': decoded_response['email'],
        'discordName': decoded_response['discordName'],
        'uid': uid
    }
    server_db.child('Students').child(decoded_response['discordName'].replace('#','_')).set(studentInformation)

def registerInstructor(uid, decoded_response):
    #put the student in the "students" section in firebase
    instructorInformation = {
        'name': decoded_response['name'],
        'email': decoded_response['email'],
        'uid': uid
    }
    server_db.child('Instructors').child(str(uid)).set(instructorInformation) 

