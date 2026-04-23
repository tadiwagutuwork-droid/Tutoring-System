import sqlite3

class DatabaseMananger:
    def __init__(self):
        self.conn = sqlite3.connect("tutoring_system.db")
        self.cursor = self.conn.cursor()
    
    def setup(self):
        self.cursor.execute("""
CREATE TABLE inquiries (
        inquiry_id TEXT PRIMARY KEY,
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
        row = inquiry.to_dict()
        self.cursor.execute("""
        INSERT INTO inquiries (
            inquiry_id, learner_name, grade, subject, 
            description, urgency, submitted_at, status, claimed_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            row['Inquiry ID'],
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
        self.conn.close()

    def search_inquiry(self):
        # Update IDs to be more simple like QMATH0001 - to make things easier
        id = input("Enter inquiry ID: ")
        self.cursor("SELECT * FROM inquiries WHERE inquiry_id = ?", (id,))
        row = self.cursor.fetchone()
        self.conn.close()
    
    def update_inquiry(self, inquiry):
        # enter what you want to update into variables to write in
        self.cursor("""
UPDATE inquiries
SET grade = ?
WHERE name = ?
""", (12, 'Tadiwa'))
        self.conn.commit()
    
    def delete_inquiry(self):
        self.cursor.execute("DELETE FROM inquiries WHERE name = ?", ("Tadiwa",))
        self.conn.commit()
        self.conn.close()
