from inquiry import Inquiry
from datetime import datetime
import json
from urgency_level import UrgencyLevel
from inquiry_status import InquiryStatus

now = datetime.now()
choice = UrgencyLevel.urg_level()
status = InquiryStatus.status_level()
tester = Inquiry('Tadiwa', 9, 'Geography', "Mapwork: Magnetic Bearing", choice, now, status)

tester.subject = 'Mathematics' 
tester.description = 'Functions: Exponential Function'
tester.claimed_by = 'Jabu'
tester.grade = 12
print(tester)

data = tester.to_dict()
data_json = json.dumps(data, indent=4)
data = tester.from_dict(data_json)
print(data)
print(tester.wait_time())

print(type(data.urgency))
print(type(data.status))
