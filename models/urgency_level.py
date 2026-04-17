from enum import IntEnum

class UrgencyLevel(IntEnum):
    CRITICAL = 1 # Exam or assessment within 24 hours.
    HIGH = 2 # Submission due within 48 hours.
    MEDIUM = 3 # General coursework difficulty.
    LOW = 4 # Conceptual curiosity, no deadline.


    @classmethod
    def urg_level(cls):
        menu = """
--- Select Urgency Level ---

1. Exam or assessment within 24 hours.
2. Submission due within 48 hours.
3. General coursework difficulty.
4. Conceptual curiosity, no deadline.

Choose option:
"""
        level = int(input(menu))
        if level not in {1, 2, 3, 4}:
            raise ValueError("Invalid value of level of urgency!")
        return cls(level)
    
    @classmethod
    def return_urgency(cls, value):
        if value not in {1, 2, 3, 4}:
            raise ValueError("Invalid value of level of urgency!")
        return cls(value)

