from operator import attrgetter
from errors import queue_error as q
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
        return self.__heap

    @heap.setter
    def heap(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__heap = value

    @property
    def history(self):
        return self.__history

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
        heapq.heappush(self.__history, value)
    
    def dequeue(self):
        self.is_empty()
        heapq.heappop(self.__heap)
    
    def peek(self):
        self.is_empty()
        return self.__heap[0]
    
    def size(self):
        self.is_empty()
        return len(self.__heap)
    
    def list_pending(self):
        self.is_empty()
        list_copy = [i for i in self.__heap if i.status == models.InquiryStatus.PENDING].sort(key=attrgetter('urgency_level', 'submitted_at'))
        return list_copy
    
    def list_all(self):
        self.is_empty_history()
        return self.__history
    
    def save(self):
        data_to_save = [item.to_dict() for item in self.__heap]
        
        if not data_to_save:
            raise q.EmptyQueueError()
        with open('inquiries.json', 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def load(self):
        with open('inquiries.json', 'r') as f:
            data = json.load(f)
        
        if not data:
            raise q.JSONFileEmptyError()
        data_to_load = [models.Inquiry.from_dict(item) for item in data]
        heapq.heapify(data_to_load)
        print(f"Successfully restored {len(data_to_load)} inquiries.")
        self.__heap = data_to_load
    