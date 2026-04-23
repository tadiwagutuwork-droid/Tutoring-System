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
        self.__cancelled = list()
        self.__claimed = list() # to handle resolved
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
    def claimed(self):
        return self.__claimed.copy()
    
    @claimed.setter
    def claimed(self, value):
        if not isinstance(value, list):
            raise q.WrongHeapError()
        self.__claimed = value

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
        value = heapq.heappop(self.__heap)
        print(self.__heap)
        value.claimed_by = tutor
        if value.status == 1:
            raise q.StatusHistoryError()
        if tutor != 'N/A' and value.status == 2:
            self.__claimed.append(value)
        else:
            heapq.heappush(self.__history, value)

    def peek(self):
        while self.heap[0].status in (4, 5):
            if self.heap[0].status == 4:
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
        self.__cancelled.append(value) 

    def resolve_inquiry(self, value):
        if value in self.claimed:
            self.claimed.discard(value)
            heapq.heappush(self.__history, value)

    def save(self):
        file_path = Path(__name__).parent.parent / "json_files" / "inquiries.json"
        if self.__heap:
            data_to_save = [item.to_dict() for item in self.heap if item.status not in (2, 4, 5)]
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        else:
            with open(file_path, 'w') as f:
                pass
        self.save_cancelled()
        self.save_claimed()
        self.save_history()

    def load(self):
        file_path = Path(__name__).parent.parent / "json_files" / "inquiries.json"
        load = []
        with open(file_path, 'r') as f:
            data = f.read().strip()
            if data:
                load = json.loads(data)
        
        if load:
            heap_to_load = [models.Inquiry.from_dict(item) for item in load]
            heapq.heapify(heap_to_load)
            print(f"Successfully restored {len(heap_to_load)} inquiries.")
            self.heap = heap_to_load
        self.load_cancelled()
        self.load_claimed()
        self.load_history()
        
    def save_cancelled(self):
        cancelled_path = Path(__name__).parent.parent / "json_files" / "cancelled.json"
        if self.__cancelled:
            cancelled_to_save = [item.to_dict() for item in self.cancelled]
            with open(cancelled_path, 'w') as f:
                json.dump(cancelled_to_save, f, indent=4)
        else:
            with open(cancelled_path, 'w') as f:
                pass

    def save_history(self):
        history_path = Path(__name__).parent.parent / "json_files" / "history.json"
        if self.__history:
            history_to_save = [item.to_dict() for item in self.history]
            with open(history_path, 'w') as f:
                json.dump(history_to_save, f, indent=4)
        else:
            with open(history_path, 'w') as f:
                pass

    def save_claimed(self):
        claimed_path = Path(__name__).parent.parent / "json_files" / "claimed.json"
        if self.__claimed:
            claimed_to_save = [item.to_dict() for item in self.claimed]
            with open(claimed_path, 'w') as f:
                json.dump(claimed_to_save, f, indent=4)
        else:
            with open(claimed_path, 'w') as f:
                pass

    def load_cancelled(self):
        cancelled_path = Path(__name__).parent.parent / "json_files" / "cancelled.json"
        load = []
        with open(cancelled_path, 'r')as f:
            data = f.read().strip()
            if data:
                load = json.loads(data)
        
        if load:
            cancelled_to_load = [models.Inquiry.from_dict(item) for item in load]
            print(f"Successfully restored {len(cancelled_to_load)} cancelled inquiries.")
            self.cancelled = cancelled_to_load

    def load_history(self):
        history_path = Path(__name__).parent.parent / "json_files" / "history.json"
        load = []
        with open(history_path, 'r')as f:
            data = f.read().strip()
            if data:
                load = json.loads(data)
        
        if load:
            history_to_load = [models.Inquiry.from_dict(item) for item in load]
            print(f"Successfully restored {len(history_to_load)} history inquiries.")
            self.history = history_to_load

    def load_claimed(self):
        claimed_path = Path(__name__).parent.parent / "json_files" / "claimed.json"
        load = []
        with open(claimed_path, 'r')as f:
            data = f.read().strip()
            if data:
                load = json.loads(data)
        
        if load:
            claimed_to_load = [models.Inquiry.from_dict(item) for item in load]
            print(f"Successfully restored {len(claimed_to_load)} claimed inquiries.")
            self.claimed = claimed_to_load
    
    def clear_json_files(self):
        with open(Path(__name__).parent.parent / "json_files" / "inquiries.json", 'w') as f:
            pass
        with open(Path(__name__).parent.parent / "json_files" / "history.json", 'w') as f:
            pass
        with open(Path(__name__).parent.parent / "json_files" / "claimed.json", 'w') as f:
            pass
        with open(Path(__name__).parent.parent / "json_files" / "cancelled.json", 'w') as f:
            pass





    