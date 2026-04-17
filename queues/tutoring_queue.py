import heapq
import models

class TutoringQueue:
    def __init__(self):
        self.__heap = list() # empty queue
        self.__history = list() # list of past inquiries
        self.__counter = None # an integer value comparing inquiries that have the same urgency but different times
    
    # implement the methods 