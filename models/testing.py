from inquiry import Inquiry
from datetime import datetime
import json

now = datetime.now()

tester = Inquiry('Tadiwa', 9, 'Geography', "Mapwork: Magnetic Bearing", 1, now, 'Juice')

tester.subject = 'Mathematics' 
tester.description = 'Functions: Exponential Function'
tester.claimed_by = 'Jabu'
tester.grade = 12
print(tester)

data = tester.to_dict()
data_json = json.dumps(data, indent=4)

print(tester.wait_time())
