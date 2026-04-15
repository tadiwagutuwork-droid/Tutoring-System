import heapq
import json
import uuid

class Inquiry:
    def __init__(self, name, subject, descri, urgency, submitted_at, status, claimed_by=None, id=None):
        self.__inquiry_id = str(uuid.uuid4()) if id is not None else None
        self.__learner_name = name
        self.__subject = subject
        self.__description = descri
        self.__urgency = urgency
        self.__submitted_at = submitted_at
        self.__status = status
        self.__claimed_by = claimed_by if claimed_by is not None else None #Tutor's name

#define getters and setters before anything else
    
    #no setter
    @property
    def inquiry_id(self):
        return self.__inquiry_id
    
    @property
    def learner_name(self):
        return self.__learner_name
    
    @property
    def subject(self):
        return self.__subject
    
    @property
    def description(self):
        return self.__description
    
    @property
    def urgency(self):
        return self.__urgency
    
    @property
    def submitted_at(self):
        return self.__submitted_at
    
    @property
    def status(self):
        return self.__status
    
    @property
    def claimed_by(self):
        return self.__claimed_by
    