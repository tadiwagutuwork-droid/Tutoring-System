import json
import uuid
from datetime import datetime
from urgency_level import UrgencyLevel
from inquiry_status import InquiryStatus

# # 1. Get current time
# now = datetime.now()

# # 2. Format it as a string
# formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

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
    def __init__(self, name, grade, subject, description, urgency, submitted_at, status, claimed_by=False, inquiry_id=False):
        super().__init__()
        self.__inquiry_id = str(uuid.uuid4()) if not id else inquiry_id
        self.__learner_name = name
        self.__grade = grade
        self.__subject = subject
        self.__description = description
        self.__urgency = urgency 
        self.__submitted_at = submitted_at # "%Y-%m-%d %H:%M:%S"
        self.__status = status
        self.__claimed_by = claimed_by if claimed_by else 'N/A' #Tutor's name

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
    
    # add setter for urgency
    @property
    def urgency(self):
        return self.__urgency
    
    @urgency.setter
    def urgency(self, value):
        if not isinstance(value, UrgencyLevel):
            raise ValueError("Invalid instance of urgency provided!")
        self.__urgency = value
    
    # add setter for submitted_at -> in case of changes
    @property
    def submitted_at(self):
        return self.__submitted_at
    
    @submitted_at.setter
    def submitted_at(self, value):
        if not isinstance(value, datetime):
            raise ValueError("Invalid format for date and time provided!")
        self.__submitted_at = value
        
    # add setter for status
    @property
    def status(self):
        return self.__status
    
    # @status.setter
    # def status(self, value):
    #     if not isinstance(value, InquiryStatus):
    #         raise ValueError("Invalid instance of status provided!")
    #     self.__status = value
        
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
        
    def to_dict(self):
        return {
            'Inquiry ID': self.__inquiry_id, 
            'Learner Name': self.__learner_name,
            'Grade': self.__grade, 
            'Subject': self.__subject,
            'Description': self.__description, 
            'Urgency': self.__urgency, 
            'Submitted At': self.__submitted_at.strftime("%Y-%m-%d %H:%M:%S"), # it is a string not an object
            'Status': self.__status, 
            #*****************************************
            'Claimed By': self.__claimed_by
        }
    
    @classmethod
    def from_dict(cls, data_string):
        # remember the cls instances
        data = json.loads(data_string) # a Python dictionary
        claimed_by = data['Claimed By'] != 'N/A'
        return cls(data['Learner Name'], data['Grade'], data['Subject'], data['Description'], UrgencyLevel.return_urgency(data['Urgency']), datetime.strptime(data['Submitted At'], "%Y-%m-%d %H:%M:%S"), InquiryStatus.return_status(data['Status']), claimed_by, True)
        
    def wait_time(self):
        """Returns how long the inquiry has been in the queue"""
        current = datetime.now()
        return current - self.__submitted_at # only do calculations with objects
    
    # Finish implementing __lt__ method
    def __lt__(self, other):
        return self.__submitted_at < other.__submitted_at
    
    def __str__(self):
        return f"""
===============  TUTORING INQUIRY ===============
Learner's Name: {self.__learner_name}
Grade: {self.__grade}
Subject: {self.__subject}
Description: {self.__description}
Urgency: {self.__urgency.name}
Submitted At: {self.__submitted_at}
Status: {self.__status.name}
Claimed By: {self.__claimed_by}
=================================================
"""
    
    def __repr__(self):
        return f"""
Inquiry(
    name={self.__learner_name}, 
    grade={self.__grade}, 
    subject={self.__subject},
    description={self.__description}, 
    urgency={self.__urgency}, 
    submitted_at={self.__submitted_at}, 
    status={self.__status}, 
    claimed_by={self.__claimed_by}
    inquiry_id={self.__inquiry_id}
    )
"""
    