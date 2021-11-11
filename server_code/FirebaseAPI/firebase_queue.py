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
        return (queue_info.get("queue", []), queue_info.get("length"))

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
        if int(current_queue_info['length']) < 1: 
            raise EmptyQueue
        else:
            ret_student = current_queue_info['queue'][0]
            current_queue_info['length'] = int(current_queue_info['length']) - 1
            current_queue_info['queue'] = current_queue_info['queue'][1:] if len(current_queue_info) >= 2 else []
            server_db.child("queue").child(class_name).set(current_queue_info)
            return ret_student



