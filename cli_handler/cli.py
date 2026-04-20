# # 1. Get current time
# now = datetime.now() -> return it like this -> submitted_at
import models as md
import queues as qu
import errors as err
from datetime import datetime, timedelta

def run():
    pass

def prompt_new_inquiry():
    pass

def display_queue():
    pass

def display_inquiry():
    pass

def prompt_urgency():
    print("""
╔══════════════════════════════════════════════════════╗
║                   URGENCY LEVEL                      ║
╠══════════════════════════════════════════════════════╣
║  [1]  CRITICAL  — Exam or assessment within 24 hrs   ║
║  [2]  HIGH      — Submission due within 48 hrs       ║
║  [3]  MEDIUM    — General coursework difficulty      ║
║  [4]  LOW       — Conceptual curiosity, no deadline  ║
╚══════════════════════════════════════════════════════╝
""")

def confirm(instance):
    pass

def show_menu():
    print("""
╔══════════════════════════════════════╗
║         TUTORING QUEUE SYSTEM        ║
╠══════════════════════════════════════╣
║  [1]  Submit new inquiry             ║
║  [2]  View pending queue             ║
║  [3]  Claim next inquiry             ║
║  [4]  Cancel an inquiry              ║
║  [5]  Quit                           ║
╚══════════════════════════════════════╝
""")

def handle_submit(instance):
    pass

def handle_claim(instance):
    pass

def handle_cancel(instance):
    pass

def handle_view(queue):
    pass

