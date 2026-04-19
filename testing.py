# Testing Tutoring System
import queues as q
import models as m
from datetime import datetime

day = datetime.now()
u = m.UrgencyLevel.return_urgency(1)
instance = m.Inquiry('Tadiwa', 8, 'Mathematics', 'Functions: Exponential', u, day)
instance.claimed_by = 'Justus'
instance.grade = 10
print(instance)
print(instance.__repr__)

queue = q.TutoringQueue()
