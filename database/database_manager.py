import sqlite3
from models import Inquiry
from errors import queue_error as q
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("tutoring_database.db")
        self.cursor = self.conn.cursor()
        self.setup()
    
    def close_connection(self):
        self.conn.close()
    
    def setup(self):
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS inquiries (
        inquiry_id TEXT,
        reference_code TEXT,
        learner_name TEXT,
        grade INTEGER,
        subject TEXT,
        description TEXT,
        urgency INTEGER,
        submitted_at TEXT,
        status INTEGER,
        claimed_by TEXT
    )
    """)
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
        inquiry_id TEXT,
        reference_code TEXT,
        learner_name TEXT,
        grade INTEGER,
        subject TEXT,
        description TEXT,
        urgency INTEGER,
        submitted_at TEXT,
        status INTEGER,
        claimed_by TEXT
    )
    """)
        self.conn.commit()

    def add_inquiry(self, inquiry):
        row = inquiry.to_database()
        self.cursor.execute("""
        INSERT INTO inquiries (
            inquiry_id, reference_code, learner_name, grade, subject, 
            description, urgency, submitted_at, status, claimed_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            row['Inquiry ID'],
            row['Reference Code'],
            row['Learner Name'],
            row['Grade'],
            row['Subject'],
            row['Description'],
            row['Urgency'],
            row['Submitted At'],
            row['Status'],
            row['Claimed By']
        ))
        self.conn.commit()
    
    def add_history(self, inquiry):
        row = inquiry.to_database()
        self.cursor.execute("""
        INSERT INTO history (
            inquiry_id, reference_code, learner_name, grade, subject, 
            description, urgency, submitted_at, status, claimed_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            row['Inquiry ID'],
            row['Reference Code'],
            row['Learner Name'],
            row['Grade'],
            row['Subject'],
            row['Description'],
            row['Urgency'],
            row['Submitted At'],
            row['Status'],
            row['Claimed By']
        ))
        self.conn.commit()

    def search_inquiry(self, reference_code, table):
        self.cursor.execute(f"SELECT * FROM {table} WHERE reference_code = ?", (reference_code,))
        row = self.cursor.fetchone()
        return Inquiry.from_database(row)
    
    def resolve_claim(self, code):
        self.cursor.execute(f"SELECT * FROM inquiries WHERE reference_code = ?", (code,))
        row = self.cursor.fetchone()
        
        if not row:
            raise ValueError('Invalid reference code')
        inquiry = Inquiry.from_database(row)
        if inquiry.submitted_at + inquiry.deadline <= datetime.now():
            self.add_history(inquiry)
            raise q.MissedInquiryError()
        inquiry.status = 3
        self.add_history(inquiry)
        self.delete_inquiry(inquiry, 'inquiries')
    
    def claim_change(self, instance):
        self.cursor.execute(f"""
UPDATE inquiries
SET status = ?, claimed_by = ?
WHERE reference_code = ?
""", (instance.status, instance.claimed_by, instance.reference_code))
        self.conn.commit()

    def cancel_inquiry(self, instance):
        self.cursor.execute(f"""
UPDATE inquiries
SET status = ?
WHERE reference_code = ?
""", (instance.status, instance.reference_code))
        self.conn.commit()

    def update_inquiry(self, inquiry, table_name):
        # enter what you want to update into variables to write in
        fields = [
    "learner_name", 
    "grade", 
    "subject", 
    "description"
]
        getter_list = [
    lambda: inquiry.learner_name,
    lambda: inquiry.grade,
    lambda: inquiry.subject,
    lambda: inquiry.description,
]
        menu = """
-----------------------------------------
      EDIT INQUIRY FIELD OPTIONS
-----------------------------------------
 1. Learner Name   
 2. Grade           
 3. Subject     
 4. Description      
-----------------------------------------
"""
        option = int(input(f"{menu}\nEnter field to change: "))
        if option not in set(range(1, 5)):
            raise ValueError("Valid innput is between 1-4")
        field_to_change = fields[option-1]
        self.cursor.execute(f"""
UPDATE {table_name}
SET {field_to_change} = ?
WHERE reference_code = ?
""", (getter_list[option-1](), inquiry.reference_code))
        self.conn.commit()
    
    def delete_inquiry(self, inquiry, table):
        self.cursor.execute(f"DELETE FROM {table} WHERE reference_code = ?", (inquiry.reference_code,))
        self.conn.commit()

    def load_database_heap(self, queue):
        query = """
SELECT * FROM inquiries 
WHERE status IN (1)
"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if not rows:
            queue.heap = []
        else:
            return_heap = list()
            for row in rows:
                return_heap.append(Inquiry.from_database(row))
            print(f"Successfully restored {len(return_heap)} inquiries.")
            queue.heap = return_heap
    
    def load_database_history(self, queue):
        query = """
SELECT * FROM history
WHERE status IN (3, 4, 5)
"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if not rows:
            queue.history = []
        else:
            return_history = list()
            for row in rows:
                return_history.append(Inquiry.from_database(row))
            print(f"Successfully restored {len(return_history)} inquiries.")
            queue.history = return_history

    def clear_database(self):
        self.cursor.execute('DELETE FROM inquiries')
        self.cursor.execute('DELETE FROM history')
        self.conn.commit()
