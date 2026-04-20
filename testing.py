from datetime import datetime, timedelta
import models
import queues


now = datetime.now()
one_hour_ago  = now - timedelta(hours=1)
yesterday     = now - timedelta(days=1)
three_days_ago = now - timedelta(days=3)

inquiries = [
    models.Inquiry('Tadiwa',  8,  'Mathematics',       'Exponential Functions', models.UrgencyLevel.return_urgency(3), three_days_ago),
    models.Inquiry('Zubair',  11, 'Physical Sciences', "Newton's Laws",         models.UrgencyLevel.return_urgency(2), one_hour_ago),
    models.Inquiry('Lindiwe',  10, 'Geography',         'Plate Tectonics',       models.UrgencyLevel.return_urgency(3), yesterday),
    models.Inquiry('Ethan',   12, 'Life Sciences',     'DNA: Code of Life',     models.UrgencyLevel.return_urgency(4), now),
]

queue = queues.TutoringQueue()
inquiries[2].claimed_by = 'Forrest'
inquiries[2].resolved()

inquiries[0].claimed_by = 'John'
inquiries[0].resolved()

inquiries[1].claimed_by = 'Leon'
inquiries[1].resolved()


inquiries[3].cancelled()


for i in inquiries: 
    queue.enqueue(i)


lst = queue.list_pending()
for l in lst:
    print(l)

data = inquiries[0].to_dict()
print(data)
f = models.Inquiry.from_dict(data)

print(inquiries[0], '*'*90, sep='\n')
print(type(f.submitted_at))
print(f.deadline)
print(queue.peek())
print(queue.size())
queue.save()
queue.load()
print(queue.heap)