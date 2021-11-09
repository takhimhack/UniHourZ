
'''
Exception thrown if the queue already exists
'''

class QueueAlreadyExists(Exception):
    def __init__(self, message="Error: the queue already exists"):
        self.message = message
        super().__init__(self.message)


class QueueDoesNotExist(Exception):
    def __init__(self, message="Error: the queue does not exist"):
        self.message = message
        super().__init__(self.message)

class EmptyQueue(Exception):
    def __init__(self, message="Error: the queue is empty."):
        self.message = message
        super().__init__(self.message)
