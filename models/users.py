from datetime import datetime
from pathlib import Path
import string
import secrets
import bcrypt

# Path(__name__).parent.parent / "database" / "reference_code.txt"
class User:
    def __init__(self, name, role, created_at=None, id=None, password_hash=None):
        def write_code(subject):
            with open(Path(__name__).parent.parent / "database" / "users_id.txt", 'r') as f:
                reader = f.read().strip()
            to_write = int(reader[-4:])+1
            with open(Path(__name__).parent.parent / "database" / "users_id.txt" , 'w') as f:
                reader = f.write(f"{to_write:04d}")
            role = 'T' if self.is_tutor(role) else 'L'
            code = f"{role}{to_write:04d}"
            return code
        
        def generate_password():
            characters = string.ascii_letters + string.digits
    
            password = ''.join(secrets.choice(characters) for _ in range(5))
            return password.upper().encode('utf-8')
        
        self.__id = write_code() if id is None else id
        self.__name = name
        if password_hash is None:
            password = generate_password()
        self.__password_hash = bcrypt.hashpw(password, bcrypt.gensalt()) if password_hash is None else password_hash
        self.__role = role.lower()
        self.__created_at = datetime.now() if created_at is not None else created_at
    
    def is_tutor(self, role):
        role = role.lower()
        return role == 'tutor'
    
    @classmethod
    def from_database(cls, data):
        return cls(data[1], data[3], data[4], data[0], data[2])

    def to_database(self):
        return {
            'ID': self.__id, 
            'Name': self.__name,
            'Password Hash': self.__password_hash,
            'Role': self.__role,
            'Created At': self.__created_at
        }
    
    def check_password(self, value):
        return self.__password_hash == value.encode('utf-8')
    
    def __str__(self):
        return f"""
Name: {self.__name}
ID: {self.__id}
Role: {self.__role}
"""