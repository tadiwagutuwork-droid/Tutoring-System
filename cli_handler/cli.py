# # 1. Get current time
# now = datetime.now() -> return it like this -> submitted_at
import models as md
import queues as qu
import errors as err
import json
from datetime import datetime, timedelta

def run():
    queue = None
    program = True
    file_path = r"C:\Users\tadvi\Tutoring-System\json_files\inquiries.json"
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        queue = qu.TutoringQueue()
    else:
        queue = qu.TutoringQueue()
        queue.load()
# ╔══════════════════════════════════════╗
# ║         TUTORING QUEUE SYSTEM        ║
# ╠══════════════════════════════════════╣
# ║  [1]  Submit new inquiry             ║
# ║  [2]  View pending queue             ║
# ║  [3]  Claim next inquiry             ║
# ║  [4]  Cancel an inquiry              ║
# ║  [5]  Quit                           ║
# ╚══════════════════════════════════════╝
    while program:
        option = int(input(f'{show_menu()}\nSelect option:'))
        if option not in set(range(1, 6)):
            raise ValueError("Invalid option selected")
        elif option == 1:
            handle_submit(queue)
        elif option == 2:
            display_queue(queue)
        elif option == 3:
            handle_claim(queue)
        elif option == 4:
            handle_cancel(queue)
        else:
            print("Thank you for using the Tutoring Queue program. Bye!")
            program = False
        queue.save()

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

def display_queue(queue):
    print(handle_view(queue))

def display_inquiry(instance):
    print(instance)

def confirm(instance):
    choice = input(f"{instance.peek()}\nConfirm inquiry (Y/N):").upper()
    if choice not in {'Y', 'N'}:
        raise ValueError('Invalid error option')
    return choice == 'Y'

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
    instance.enqueue(prompt_new_inquiry())

def handle_claim(instance):
    tutor_name = input("Enter tutor's name:").strip().title()
    x = instance.peek()
    display_inquiry(x)
    if confirm():
        instance.dequeue(tutor_name)
    else:
        print("INQUIRY NOT HANDLED")

def handle_cancel(queue):
    inquiry = get_name_queue()
    inquiry.cancelled()
    queue.cancelled_set(inquiry)

def handle_view(queue):
    lst = queue.list_pending()
    widths = {
    'Inquiry ID': 12,
    'Learner Name': 18,
    'Grade': 8,
    'Subject': 12,
    'Urgency': 10,
    'Status': 10,
    'Claimed By': 15
}
    header = "".join([f"{key:<{widths[key]}} | " for key in widths])
    separator = "-" * (sum(widths.values()) + (len(widths) * 3))
    row_strings = []
    for item in lst:
        item = item.to_dict()
        row = "".join([f"{str(item.get(key, '')):<{widths[key]}} | " for key in widths])
        row_strings.append(row)

    final_table = f"{header}\n{separator}\n" + "\n".join(row_strings)
    return final_table

def get_name_queue(instance):
    name = prompt_name()
    inquiry = instance.get_instance(name)
    return inquiry



