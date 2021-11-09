from firebaseAPI import *
import firebase_queue as fb
from queue_exceptions.queue_exceptions import *
'''
This is the testing suite for the firebase queue functionality. 
Each test that adds to the firebase will also remove from the firebase
'''

'''
passes if a queue was created successfully
'''
def should_create_queue():
    try:
        fb.create_queue("cse 354")
        server_db.child("queue").child("cse 354").remove()
        print("should_create_queue() passed!")
    
    except QueueAlreadyExists:
        print("Test failed: Function raised QueueAlreadyExists, but the queue didn't exist")

    except Exception as e:
        print("Error, test failed: " + str(e))



def should_fail_to_create_same_queue():
    try:
        fb.create_queue("cse 354")
        fb.create_queue("cse 354")
        print("Test failed: the queue already existed, but no error was thrown.")

    except QueueAlreadyExists:
        print("should_fail_to_create_same_queue() passed!")
        server_db.child("queue").child("cse 354").remove()

def should_fail_to_access_queue():
    try:
        fb.access_queue("cse 354")
        print("Test failed: there exists no cse 354 queue")
    
    except QueueDoesNotExist:
        print("should_fail_to_access_queue() passed!")
    
    except Exception as e:
        print("Error, test failed: " + str(e))

def should_access_queue():
    try:
        fb.create_queue("cse 354")
        ls = fb.access_queue("cse 354")
        print("should_access_queue() passed! " + str(ls))
        server_db.child("queue").child("cse 354").remove()
    
    except QueueDoesNotExist:
        print("Test failed: The queue cse 354 exists!")
    
    except Exception as e:
        print("Error, test failed: " + str(e))


def should_fail_to_enqueue():
    try:
        fb.enqueue_student("cse 354", "chandra", "cpneppal")
        print("Test failed: Enqueue worked when it shouldn't have")
    
    except QueueDoesNotExist:
        print("should_fail_to_enqueue() passed!")

    except Exception as e:
        print("Error, test failed: " + str(e))

def should_enqueue_students():
    try:
        expected_result = (
            [
                {'name': 'cpneppal', 'ubit': 'chandra'}, 
                {'name': 'tolo', 'ubit': 'john'}, 
                {'name': 'bird', 'ubit': 'amazing'}
            ],
            3
        )
        fb.create_queue("cse 354")
        fb.enqueue_student("cse 354", "chandra", "cpneppal")
        fb.enqueue_student("cse 354", "john", "tolo")
        fb.enqueue_student("cse 354", "amazing", "bird")
        queue_access = fb.access_queue("cse 354")
        if queue_access[1] != 3:
            print("Test failed: the length of the queue returned wasn't 3")        
        for i in range(3):
            if expected_result[0][i]['name'] != queue_access[0][i]['name'] or \
                expected_result[0][i]['ubit'] != queue_access[0][i]['ubit']:
                print(f"Test failed: The queue elements did not match: \
                    {expected_result[0][i]['name']} != {queue_access[0][i]['name']} or \
                     {expected_result[0][i]['ubit']}!= {queue_access[0][i]['ubit']}")
                break
        print("should_enqueue_students() passed!")
        server_db.child("queue").child("cse 354").remove()
    
    except QueueDoesNotExist:
        print("Test failed: A queue exists, but enqueue failed")

    except Exception as e:
        print("Error, test failed: " + str(e))

def should_fail_to_dequeue_non_existent_queue():
    try:
        fb.dequeue_student("cse 354")
        print("Test failed: Dequeued a non existent queue")

    except QueueDoesNotExist:
        print("should_fail_to_dequeue_non_existent_queue() passed!")
    
    except Exception as e:
        print("Error, test failed: " + str(e))

def should_fail_to_dequeue_empty_queue():
    try:
        fb.create_queue("cse 354")
        fb.dequeue_student("cse 354")
        print("Test failed: Dequeued a non existent queue")
    except EmptyQueue:
        print("should_fail_to_dequeue_empty_queue() passed!")
        server_db.child("queue").child("cse 354").remove()
    except Exception as e:
        print("Error, test failed: " + str(e)) 
    
def should_dequeue_one_student():
    try:
        fb.create_queue("cse 354")
        fb.enqueue_student("cse 354", "cpneppal", "chandra")
        ret_student = fb.dequeue_student("cse 354")
        retQueue = fb.access_queue("cse 354")
        if len(retQueue[0]) != 0 or retQueue[1] != 0:
            print("Test failed: Queue was not properly updated!")
        
        elif ret_student['name'] != "chandra" or ret_student['ubit'] != "cpneppal":
            print("Test failed: Incorrect Data was returned!")
        
        else:
            print("should_dequeue_one_student() passed!")
        server_db.child("queue").child("cse 354").remove()   
    except EmptyQueue:
        print("Test failed: The Queue isn't empty")
    
    except Exception as e:
        print("Error, test failed: " + str(e)) 

def should_dequeue_student():
    try:
        fb.create_queue("cse 354")
        fb.enqueue_student("cse 354", "cpneppal", "chandra")
        fb.enqueue_student("cse 354", "john", "tolo")
        ret_student = fb.dequeue_student("cse 354")
        retQueue = fb.access_queue("cse 354")
        if len(retQueue[0]) != 1 or retQueue[0][0]["ubit"] != "john" \
            or retQueue[0][0]["name"] != "tolo"  or retQueue[1] != 1:
            print("Test failed: Queue was not properly updated!")
        
        elif ret_student['name'] != "chandra" or ret_student['ubit'] != "cpneppal":
            print("Test failed: Incorrect Data was returned!")
        
        else:
            print("should_dequeue_one_student() passed!")
        server_db.child("queue").child("cse 354").remove()   
    except EmptyQueue:
        print("Test failed: The Queue isn't empty")
    
    except Exception as e:
        print("Error, test failed: " + str(e)) 

if __name__ == "__main__":
    should_create_queue()
    should_fail_to_create_same_queue()
    should_fail_to_access_queue()
    should_access_queue()
    should_fail_to_enqueue()
    should_enqueue_students()
    should_fail_to_dequeue_non_existent_queue()
    should_fail_to_dequeue_empty_queue()
    should_dequeue_one_student()
    should_dequeue_student()