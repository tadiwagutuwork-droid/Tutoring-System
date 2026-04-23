from cli_handler import cli
from models import Inquiry, UrgencyLevel
from datetime import datetime

instance = Inquiry('Tadiwa', 9, 'Mathematics', 'Functions', UrgencyLevel(3), datetime.now())

g = instance.to_dict()
print(g)

print(type(g['Urgency']))