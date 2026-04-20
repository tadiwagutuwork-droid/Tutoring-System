from datetime import datetime, timedelta
import models
import queues

now = datetime.now()
one_hour_ago  = now - timedelta(hours=1)
yesterday     = now - timedelta(days=1)
three_days_ago = now - timedelta(days=3)

inquiries = [
    models.Inquiry('Tadiwa',  8,  'Mathematics',       'Exponential Functions', 1, three_days_ago),
    models.Inquiry('Zubair',  11, 'Physical Sciences', "Newton's Laws",         2, one_hour_ago),
    models.Inquiry('Lindiwe', 10, 'Geography',         'Plate Tectonics',       3, yesterday),
    models.Inquiry('Ethan',   12, 'Life Sciences',     'DNA: Code of Life',     4, now),
]

queue = queues.TutoringQueue()

for i in inquiries:
    queue.enqueue(i)

print(queue.heap)
print(queue.dequeue())
print(queue.heap)

