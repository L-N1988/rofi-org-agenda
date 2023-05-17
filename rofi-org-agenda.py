import orgparse
import Orgmode
import datetime
from rofi import Rofi

# path to where you want your TODOs to be inserted to
inbox_file = "/home/liuning/org/TODO.org"
r = Rofi()
nodes = Orgmode.makelist(inbox_file)
today = datetime.date.today()

todos = []
todos_today = []
for node in nodes:
    if node.Todo() == 'TODO':
        todos.append(node.Heading())
        if node.Scheduled() == today:
            todos_today.append(node.Heading())

index, key = r.select('ORG-TODO', todos, key1=('Alt+a', "Agenda for current week or day"))
print(index, key)
if key == 1:
    r.select('AGENDA-TODAY', todos_today, message='<b>TODO</b>\t \t \t Date')
