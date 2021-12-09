from server_code.FirebaseAPI.firebaseAPI import *
from server_code.FirebaseAPI.queue_exceptions.queue_exceptions import *

'''
params: class_name: string
return val: None or Exception thrown if queue already exists.
'''
def create_queue(class_name):
    #if the queue doesn't exist, or the class_name's data doesn't exist, then we create the queue
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        queue_info = {
            "length": 0,
            "queue": []
        }
        server_db.child("queue").child(class_name).set(queue_info)
    else:
        raise QueueAlreadyExists

'''
params: class_name: string
return val: A list of student dictionaries representing the queue of students
'''
def access_queue(class_name):
    #if the queue doesn't exist, we throw an exception
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        raise QueueDoesNotExist
    else:
        queue_info = server_db.child("queue").child(class_name).get().val()
        return (queue_info.get("queue", []), queue_info.get("length"), queue_info.get("instructor"), queue_info.get("location"), queue_info.get("eta"), queue_info.get("student"), queue_info.get("status"))

'''
params: class_name: string
return val: A list of student dictionaries representing the queue of students
'''
def access_user(discord_tag):
    #if the user doesn't exist, we throw an exception
    if(server_db.child("Students").get().val() is None or server_db.child("Students").child(discord_tag).get().val() is None):
        raise UserDoesNotExist
    else:
        user_info = server_db.child("Students").child(discord_tag).get().val()
        return (user_info.get("name"))


'''
params: class_name: string
return val: A list of queue status, eta/time per student, length of queue.
'''
def access_course(class_name):
    #if the queue doesn't exist, we throw an exception
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        raise QueueDoesNotExist
    else:
        queue_info = server_db.child("queue").child(class_name).get().val()
        return (queue_info.get("status"), queue_info.get("eta"), queue_info.get("length"), queue_info.get("queue", []))

'''
params: class_name: string
return val: Nothing
'''
def leave_queue(class_name, discord_tag):
    #if the queue doesn't exist, we throw an exception
    print(discord_tag)
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        raise QueueDoesNotExist
    else:
        current_queue_info = server_db.child("queue").child(class_name).get().val()
        current_queue_info['length'] = max(int(current_queue_info['length']) - 1, 0)
        new_queue_list = []
        for user in current_queue_info.get('queue', []):
          if user['name'] != str(discord_tag):
            new_queue_list.append(user)
        current_queue_info['queue'] = new_queue_list
        server_db.child("queue").child(class_name).set(current_queue_info)

'''
params: class_name: string, ubit_student: string, name: string
return val: Nothing
'''

def enqueue_student(class_name, ubit_student, name):
    #if the queue doesn't exist, we throw an exception. Else, add to the queue and update its length.
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        raise QueueDoesNotExist
    else:
        current_queue_info = server_db.child("queue").child(class_name).get().val()
        current_queue_info['length'] = int(current_queue_info['length']) + 1
        current_queue_info['queue'] = current_queue_info.get('queue', []) + [{"ubit": ubit_student, "name": name}]
        server_db.child("queue").child(class_name).set(current_queue_info)

'''
params: class_name: string
return val: Nothing
'''
def dequeue_student(class_name):
    #if the queue doesn't exist, we throw an exception. Else, add to the queue and update its length.
    if(server_db.child("queue").get().val() is None or server_db.child("queue").child(class_name).get().val() is None):
        raise QueueDoesNotExist
    else:
        current_queue_info = server_db.child("queue").child(class_name).get().val()
        if int(current_queue_info['length']) < 1 and current_queue_info['student'] == "":
            raise EmptyQueue
        elif int(current_queue_info['length']) < 1:
            current_queue_info['student'] = ""
            server_db.child("queue").child(class_name).set(current_queue_info)
            return ""
        else:
            ret_student = current_queue_info['queue'][0]
            current_queue_info['length'] = max(int(current_queue_info['length']) - 1, 0)
            current_queue_info['student'] = ret_student['name']
            current_queue_info['queue'] = current_queue_info['queue'][1:] if len(current_queue_info) >= 2 else []
            server_db.child("queue").child(class_name).set(current_queue_info)
            return ret_student

def change_queue_settings(settings):
    if server_db.child("queue").get().val() is None or server_db.child("queue").child(settings["class"]).get().val() is None:
        raise QueueDoesNotExist
    else:
        current_queue_info = server_db.child("queue").child(settings["class"]).get().val()
        current_queue_info["status"] = settings["status"]
        if settings["status"] == "closed":
            current_queue_info["student"] = ""
            current_queue_info["length"] = 0
            current_queue_info["queue"] = []
        current_queue_info["eta"] = settings["eta"]
        current_queue_info["instructor"] = settings["instructor"]
        current_queue_info["location"] = settings["location"]
        server_db.child("queue").child(settings["class"]).set(current_queue_info)


def is_instructor(uid):
    if server_db.child("Instructors").get().val() is None or server_db.child("Instructors").child(uid).get().val() is None:
        return False
    return True
