# # 1. Get current time
# now = datetime.now() -> return it like this -> submitted_at
import models as md
import queues as qu
import errors as err
from datetime import datetime, timedelta

def run():
    pass

def prompt_new_inquiry():
    name = prompt_name()
    grade = prompt_grade()
    subject = prompt_subject(grade)
    description = prompt_description()
    urgency = prompt_urgency()
    date = datetime.now()
    
    return md.Inquiry(name, grade, subject, description, urgency, date)

def prompt_name():
    get_name = input("Enter learner's name:").strip()
    if get_name == '':
        raise ValueError("No empty names allowed")
    return get_name.title()

def prompt_grade():
    get_grade = int(input("Enter learner's grade:"))
    if get_grade not in md.Attributes().grades:
        raise ValueError("Invalid grade entry")
    return get_grade

def prompt_subject(grade):
    subject_menu = """
╔══════════════════════════════════════════════════════╗
║                    SUBJECTS                          ║
╠══════════════════════════════════════════════════════╣
║  [1]  Mathematics                                    ║
║  [2]  Physical Sciences                              ║
║  [3]  Geography                                      ║
║  [4]  Life Sciences                                  ║
║  [5]  Natural Sciences                               ║
╚══════════════════════════════════════════════════════╝
"""
    option = input(f"{subject_menu}\nSelect option:")
    lst = list(md.Attributes().subject_index)
    if option not in md.Attributes().subject_index:
        raise ValueError("Invalid option provided!")
    get_subject= lst[option-1]
    if grade not in md.Attributes().subject_index.get(get_subject):
        raise ValueError('No grade in subject!')
    return get_subject
    
def prompt_description():
    get_description = input("Enter description of inquiry:").strip().capitalize()
    return get_description

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
    choice = int(input("Select urgency level [1-4]:"))
    if choice not in {1, 2, 3, 4}:
        raise err.queue_error.ChoiceError()
    return md.UrgencyLevel(choice)

def display_queue():
    pass

def display_inquiry():
    pass

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

