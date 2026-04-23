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
        urgency TEXT,
        submitted_at TEXT,
        status TEXT,
        claimed_by TEXT
    )
    """)
        
        self.conn.commit()

    def add_inquiry(self):
        self.cursor.execute()


