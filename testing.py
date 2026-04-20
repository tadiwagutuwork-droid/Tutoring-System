# Testing Tutoring System
import queues as q
import models as m
from datetime import datetime, timedelta

day = datetime.now()
instance_1 = m.Inquiry('Tadiwa', 8, 'Mathematics', 'Functions: Exponential', m.UrgencyLevel.return_urgency(1), day)
instance_2 = m.Inquiry('Zubair', 11, 'Physical Sciences', 'Newton’s Laws of Motion', m.UrgencyLevel.return_urgency(4), day)
instance_3 = m.Inquiry('Lindiwe', 10, 'Geography', 'Plate Tectonics', m.UrgencyLevel.return_urgency(4), day)
instance_5 = m.Inquiry('Sarah', 9, 'English', 'Poetry Analysis', m.UrgencyLevel.return_urgency(3), day)
instance_1.claimed_by = 'Justus'
instance_1.grade = 10

instance_2.change_urgency()
queue = q.TutoringQueue()
queue.enqueue(instance_1)
queue.enqueue(instance_2)
queue.enqueue(instance_3)
queue.enqueue(instance_5)


instance_1.change_urgency()
instance_1.change_deadline()
print(instance_1)
