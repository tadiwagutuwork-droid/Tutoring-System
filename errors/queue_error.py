class QueueError(Exception):
    def __init__(self):
        pass

class EmptyQueueError(QueueError):
    def __init__(self, message="Action failed: The tutoring queue is currently empty."):
        self.message = message
        super().__init__(self.message)

class InquiryNotFoundError(QueueError):
    def __init__(self, message='Inquiry ID was not found in the system.'):
        self.message = message
        super().__init__(self.message)

class InvalidUrgencyError(QueueError):
    def __init__(self, message='Invalid urgency. Please use: 1, 2, 3, or 4'):
        self.message = message
        super().__init__(self.message)

class InvalidStatusError(QueueError):
    def __init__(self, message='Invalid status. Please use: 1, 2, 3, or 4'):
        self.message = message
        super().__init__(self.message)

class JSONFileEmptyError(QueueError):
    def __init__(self, message='Empty JSON file Found!'):
        self.message = message
        super().__init__(self.message)

class HistoryQueueEmptyError(QueueError):
    def __init__(self, message='History Queue Empty Error!'):
        self.message = message
        super().__init__(self.message)

class WrongInstanceError(QueueError):
    def __init__(self, value):
        self.message = f"Invalid instance of {value.title()} class"
        super().__init__(self.message)