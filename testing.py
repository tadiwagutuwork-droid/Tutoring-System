from cli_handler import cli
from models import Inquiry, UrgencyLevel
from datetime import datetime
from pathlib import Path

instance = Inquiry('Tadiwa', 9, 'Mathematics', 'Functions', UrgencyLevel(3), datetime.now())
print(type(instance.urgency.value))
# g = instance.to_dict()
# print(g)

# print(type(g['Urgency']))

# def write_code(subject):
#     with open(Path(__name__).parent.parent / "database" / "reference_code.txt", 'r') as f:
#         reader = f.read().strip()
#         if reader == '99999':
#             reader = '00000'
#     code = f"QMATH{int(reader[-4:])+1:05d}"
#     with open(Path(__name__).parent.parent / "database" / "reference_code.txt", 'w') as f:
#         writer = f.write(f"{int(reader[-4:])+1:05d}")
#     return code

# print(write_code('pooo'))