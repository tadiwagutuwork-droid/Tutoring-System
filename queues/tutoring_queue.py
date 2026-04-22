from operator import attrgetter
from errors import queue_error as q
import heapq
import models
import json

class TutoringQueue:
    def __init__(self):
        self.__heap = list() # empty queue
        self.__history = list() # list of past inquiries
        self.__cancelled = set()
        self.__claimed = set() # to handle resolved
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
    def cancelled(self):
        if not self.__cancelled:
            return "Heap is empty"
        return self.__cancelled

    @cancelled.setter
    def cancelled(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__cancelled = value

    @property
    def history(self):
        self.is_empty_history()
        return self.__history.copy()
    
    @history.setter
    def history(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__history = value

    @property
    def resolved(self):
        return self.__resolved.copy()
    
    @resolved.setter
    def resolved(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__resolved = value

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
    
    def dequeue(self, tutor='N/A'):
        value = heapq.heappop(self.heap)
        value.claimed_by = tutor
        if value.status == 1:
            raise q.StatusHistoryError()
        heapq.heappush(self.__history, value)
    
    def peek(self):
        while self.heap[0].status == 5:
            self.cancelled_set(self.heap[0])
            self.dequeue()
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
    
    def save(self):
        data_to_save = [item.to_dict() for item in self.heap if item.status != 5]
        history_to_save = [item.to_dict() for item in self.history]
        skip = False
        if not data_to_save:
            raise q.EmptyQueueError()
        elif not history_to_save:
            skip = True
        file_path = r"C:\Users\tadvi\Tutoring-System\json_files\inquiries.json"
        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        if not skip:
            history_path = r"C:\Users\tadvi\Tutoring-System\json_files\history.json"
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=4)

    def load(self):
        file_path = r"C:\Users\tadvi\Tutoring-System\json_files\inquiries.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        history_path = r"C:\Users\tadvi\Tutoring-System\json_files\history.json"
        with open(file_path, 'r') as f:
            history = f.read().strip()
            if not history:
                history = []
            else:
                history = json.loads(history)
        
        if history:
            history_to_load = [models.Inquiry.from_dict(item) for item in history]
            print(f"Successfully restored {len(history_to_load)} inquiries.")
            self.history = history_to_load

        if not data:
            raise q.JSONFileEmptyError()
        data_to_load = [models.Inquiry.from_dict(item) for item in data]
        heapq.heapify(data_to_load)
        print(f"Successfully restored {len(data_to_load)} inquiries.")
        self.heap = data_to_load

    def get_instance(self, value):
        self.is_empty()
        for instance in self.__heap:
            if value == instance.learner_name:
                return instance
        else:
            raise ValueError("Name not Found")
        
    def cancelled_set(self, value):
        if not isinstance(value, models.Inquiry) and value.status != 5:
            raise q.WrongInstanceError()
        self.__cancelled.add(value)

    def save_cancelled(self):
        pass

    def save_history(self):
        pass

    def save_resolved(self):
        pass

    def load_cancelled(self):
        pass

    def load_history(self):
        pass

    def load_resolved(self):
        pass



    