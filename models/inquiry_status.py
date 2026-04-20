from enum import IntEnum
from errors import queue_error as q

class InquiryStatus(IntEnum):
    PENDING = 1 # In the queue, not yet claimed.
    CLAIMED = 2 # A tutor has dequeued and is actively handling it.
    RESOLVED = 3 # The inquiry has been answered and closed.
    CANCELLED = 4 # The learner withdrew the inquiry.
    MISSED = 5

    @classmethod
    def status_level(cls):
        menu = """
--- Select Status ---

1. In the queue, not yet claimed.
2. A tutor has dequeued and is actively handling it.
3. The inquiry has been answered and closed.
4. The learner withdrew the inquiry.

Choose option:
"""
        level = int(input(menu))
        if level not in {1, 2, 3, 4, 5}:
            raise q.InvalidStatusError()
        return cls(level)
    
    @classmethod
    def return_status(cls, value):
        if value not in {1, 2, 3, 4, 5}:
            raise q.InvalidStatusError()
        return cls(value)

