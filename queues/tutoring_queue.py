from operator import attrgetter
from errors import queue_error as q
from pathlib import Path
import heapq
import models
import json

class TutoringQueue:
    def __init__(self):
        self.__heap = list() # empty queue
        self.__history = list() # list of past inquiries
        # use this format to ensure FIFO (Urgency Level, Datetime Object, Inquiry Object)
    # implement the methods 

    @property
    def heap(self):
        self.is_empty()
        return self.__heap.copy()

    @heap.setter
    def heap(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__heap = value

    @property
    def history(self):
        self.is_empty_history()
        return self.__history.copy()
    
    @history.setter
    def history(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__history = value

    def verify_object(self, value):
        if not isinstance(value, models.Inquiry):
            raise q.WrongInstanceError('Inquiry')
   
    def is_empty(self):
        if not self.__heap:
            raise q.EmptyQueueError()
    
    def is_empty_history(self):
        if not self.__history:
            raise q.HistoryQueueEmptyError()
        
    def enqueue(self, value):
        self.verify_object(value)
        heapq.heappush(self.__heap, value)
    
    def dequeue(self, db, tutor='N/A'):
        value = heapq.heappop(self.__heap)
        value.claimed_by = tutor
        db.delete_inquiry(value, 'inquiries')
        if value.status == 1:
            raise q.StatusHistoryError()
        elif value.status == 2:
            db.add_claimed(value)
            return value
        else:
            db.add_history(value)
            heapq.heappush(self.__history, value)

    def peek(self, db):
        while self.heap[0].status in (4, 5):
            self.dequeue(db)
        return self.heap[0]
    
    def size(self):
        self.is_empty()
        return len(self.__heap)
    
    def list_pending(self, value=False):
        heap = self.heap
        list_copy = sorted([i for i in heap if i.status == 1], key=attrgetter('urgency', 'submitted_at'))
        return list_copy
    
    def list_all(self):
        for h in self.history:
            print(h, end='\n')
        
   