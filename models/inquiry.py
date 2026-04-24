import json
import uuid
from datetime import datetime, timedelta
from .urgency_level import UrgencyLevel
from .inquiry_status import InquiryStatus
from errors import queue_error as q
from pathlib import Path

# # 1. Get current time
# now = datetime.now()

# # 2. Format it as a string
# formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

#status -> InquiryStatus
class Attributes:
    """ For O(1) searching -> faster algorithm """
    def __init__(self):
        self.__grades = {7, 8, 9, 10, 11, 12}
        self.__subject_index = {'Mathematics': [set(range(7, 13)), 'QMATH'], 
                                'Physical Sciences': [set(range(10, 13)), 'QPHYS'], 
                                'Geography': [set(range(7, 13))], 
                                'Life Sciences': [set(range(10, 13)), 'QLFSC'], 
                                'Natural Sciences': [set(range(7, 10)), 'QNSCI'],
                                'English': [set(range(7, 13)), 'QENGL']
                                }
    
    @property
    def grades(self):
        return self.__grades
    
    @property
    def subject_index(self):
        return self.__subject_index

class Inquiry(Attributes):
    def __init__(self, name, grade, subject, description, urgency, submitted_at, claimed_by=False, inquiry_id=str(uuid.uuid4()), status=InquiryStatus(1), reference_code=None):
        super().__init__()
        def write_code(subject):
            with open(Path(__name__).parent.parent / "database" / "reference_code.txt", 'r') as f:
                reader = f.read().strip()
            to_write = int(reader[-4:])+1
            with open(Path(__name__).parent.parent / "database" / "reference_code.txt", 'w') as f:
                reader = f.write(f"{to_write:05d}")
            code = f"{self.subject_index.get(subject)[1]}{to_write:05d}"
            return code
        
        def check_deadline(value):
            if value == 1:
                return timedelta(hours=24)
            elif value == 2:
                return timedelta(hours=48)
            elif value == 3:
                return timedelta(hours=72)
            else:
                return timedelta(hours=96)
            
        self.__inquiry_id = inquiry_id
        self.__learner_name = name
        self.__grade = grade
        self.__subject = subject
        self.__reference_code = write_code(subject) if reference_code is None else reference_code
        self.__description = description
        self.__urgency = urgency 
        self.__submitted_at = submitted_at # "%Y-%m-%d %H:%M:%S"
        self.__status = status
        self.__claimed_by = claimed_by if isinstance(claimed_by, str) else 'N/A' #Tutor's name
        value = self.__urgency
        self.__deadline = check_deadline(value)
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
            if value not in {1, 2, 3, 4}:
                raise q.InvalidUrgencyError()
            value = UrgencyLevel.return_urgency(value)
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
    
    @status.setter
    def status(self, value):
        if not isinstance(value, InquiryStatus):
            if value not in {1, 2, 3, 4, 5}:
                raise q.InvalidStatusError()
            value = InquiryStatus.return_status(value)
        self.__status = value
        
    @property
    def claimed_by(self):
        return self.__claimed_by
    
    @claimed_by.setter
    def claimed_by(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid name given!")
        self.__claimed_by = value.title()
        self.status = InquiryStatus.return_status(2) # CLAIMED

    @property
    def deadline(self):
        return self.__deadline
    
    @deadline.setter
    def deadline(self, value):
        if not isinstance(value, timedelta):
            raise ValueError("Value not type of datetime")
        if self.__urgency == 1 and value > timedelta(hours=24):
            raise q.TimeError()
        elif self.__urgency == 2 and (value > timedelta(hours=48) or  value < timedelta(hours=24)):
            raise q.TimeError()
        elif self.__urgency in (3, 4) and (value < timedelta(hours=48)):
            raise q.TimeError()
        self.__deadline = value

    @property
    def reference_code(self):
        return self.__reference_code
    
    # Methods
    def verify_subject(self, grade):
        grades = self.subject_index.get(self.__subject, -1)
        if grades != -1:
            if grade not in grades[0]: # -> a set is returned so time complexity is O(n)
                raise ValueError(f"No grade {grade} in {self.__subject}!")
            
    def verify_grade(self, subject):
        if subject.title() not in self.subject_index:
            raise ValueError(f"{subject.title()} not found in subjects of grade!")
        
    def to_database(self):
        return {
            'Inquiry ID': self.__inquiry_id, 
            'Reference Code': self.__reference_code,
            'Learner Name': self.__learner_name,
            'Grade': self.__grade, 
            'Subject': self.__subject,
            'Description': self.__description, 
            'Urgency': self.__urgency.value, 
            'Submitted At': self.__submitted_at.strftime("%Y-%m-%d %H:%M:%S"), # it is a string not an object
            'Status': self.__status.value, 
            #*****************************************
            'Claimed By': self.__claimed_by
        }
    
    @classmethod
    def from_database(cls, data):
        # remember the cls instances
        claimed_by = data[9] if data[9] != 'N/A' else False
        return cls(data[2], data[3], data[4], data[5], UrgencyLevel.return_urgency(data[6]), datetime.strptime(data[7], "%Y-%m-%d %H:%M:%S"), claimed_by, data[0], InquiryStatus.return_status(data[8]), data[1])
        
    def wait_time(self):
        """Returns how long the inquiry has been in the queue"""
        current = datetime.now()
        return current - self.__submitted_at # only do calculations with objects
    
    def change_urgency(self):
        wait = self.wait_time()
        if wait <= timedelta(hours=24):
            self.urgency = 1
            self.deadline = timedelta(hours=24)
        elif wait <= timedelta(hours=48):
            self.urgency = 2
            self.deadline = timedelta(hours=48)
        elif wait <= timedelta(hours=72):
            self.urgency = 3
            self.deadline = timedelta(hours=72)
        elif wait <= timedelta(hours=96):
            self.urgency = 4
            self.deadline = timedelta(hours=96)
        self.change_deadline()

    def change_deadline(self):
        wait = self.wait_time()
        print(self.deadline , wait)
        if self.deadline < wait and self.__status != 3:
            self.status = 5

    def cancelled(self):
        self.status = 5

    # Finish implementing __lt__ method
    def __lt__(self, other):
        if self.__urgency == other.__urgency:
            if self.__submitted_at == other.__submitted_at:
                return self.__learner_name < other.__learner_name
            return self.__submitted_at < other.__submitted_at
        return self.__urgency < other.__urgency
    
    def __str__(self):
        return f"""
===============  TUTORING INQUIRY ===============
Reference Code: {self.__reference_code}
Learner's Name: {self.__learner_name}
Grade: {self.__grade}
Subject: {self.__subject}
Description: {self.__description}
Urgency: {self.__urgency.name}
Submitted At: {self.__submitted_at.strftime("Date: %Y-%m-%d || Time: %H:%M:%S")[:34]}
Status: {self.__status.name}
Claimed By: {self.__claimed_by}
Deadline: {self.__deadline}
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
    reference_code={self.__reference_code}
    )
"""

    