import heapq
import models

class TutoringQueue:
    def __init__(self):
        self.__heap = list() # empty queue
        self.__history = list() # list of past inquiries
        self.__counter = None # an integer value comparing inquiries that have the same urgency but different times
        # use this format to ensure FIFO (Urgency Level, Datetime Object, Inquiry Object)
    # implement the methods 

# Now you can just push the object directly!
# def __lt__(self, other):
#         # First, compare urgency
#         if self.urgency.value != other.urgency.value:
#             return self.urgency.value < other.urgency.value
#         # If urgency is tied, compare timestamps (FIFO)
#         return self.submitted_at < other.submitted_at

# Now you can just push the object directly!
# heapq.heappush(queue, my_inquiry)