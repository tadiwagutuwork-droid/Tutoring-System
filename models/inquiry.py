import heapq
import json
import uuid

#status -> InquiryStatus
class Attributes:
    """ For O(1) searching -> faster algorithm """
    def __init__(self):
        self.__grades = {7, 8, 9, 10, 11, 12}
        self.__subject_index = {'Mathematics': {7, 8, 9, 10, 11, 12}, 
                                'Physical Sciences': {10, 11, 12}, 
                                'Geography': {7, 8, 9, 10, 11, 12}, 
                                'Life Sciences': {10, 11, 12}, 
                                'Natural Sciences': {7, 8, 9}
                                }
    
    @property
    def grades(self):
        return self.__grades
    
    @property
    def subject_index(self):
        return self.__subject_index


class Inquiry(Attributes):
    def __init__(self, name, grade, subject, descri, urgency, submitted_at, status, claimed_by=None, id=None):
        super().__init__()
        self.__inquiry_id = str(uuid.uuid4()) if id is not None else None
        self.__learner_name = name
        self.__grade = grade
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
    
    @learner_name.setter
    def learner_name(self, value):
        if not isinstance(value, str) and value == '':
            raise ValueError("Invalid name given!")
        self.__learner_name = value.title()

    @property
    def grade(self):
        return self.__grade
    
    @grade.setter
    def grade(self, value):
        if not (isinstance(value, (int, str, float)) and int(value) in self.grades):
            raise ValueError("Invalid grade given!")
        self.verify_subject(int(value))
        self.__grade = int(value)
    
    @property
    def subject(self):
        return self.__subject
    
    @subject.setter
    def subject(self, value):
        #Have subject set or dictionary for subjects you offer and verify with grade too
        if not (isinstance(value, str) and value.title() in self.subject_index):
            raise ValueError("Invalid subject given!")
        self.verify_grade(value)
        self.__subject = value.title()
    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid description given!")
        self.__description = value.capitalize()
    
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
    
    @claimed_by.setter
    def claimed_by(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid name given!")
        self.__claimed_by = value.title()
    
    # Methods
    def verify_subject(self, grade):
        grades = self.subject_index.get(self.__subject, -1)
        if grades != -1:
            if grade not in grades: # -> a set is returned so time complexity is O(n)
                raise ValueError(f"No grade {grade} in {self.__subject}!")
            
    def verify_grade(self, subject):
        if subject.title() not in self.subject_index:
            raise ValueError(f"{subject.title()} not found in subjects!")
        




        
    