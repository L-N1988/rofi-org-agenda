import orgparse
import Orgmode
import rofi_org_todo
import datetime as dt
from rofi import Rofi
import bisect

# change this to align output strings
MAX_LINE_CHAR = 55 # approx max chars number in one line of rofi

# path to where you want your TODOs to be inserted to
inbox_file = "/home/liuning/org/TODO.org"
r = Rofi()
nodes = Orgmode.makelist(inbox_file)
today = dt.date.today()

todos = []
todos_today = []
sch_list = []
for node in nodes:
    if node.Todo() == 'TODO':
        if node.Scheduled() == "":
            todos.append(node.Heading())
        else:
            # Find the index where the new item should be inserted
            index = bisect.bisect(sch_list, node.Scheduled())
            # Insert the new item into the list at the correct position
            sch_list.insert(index, node.Scheduled())
            todos.insert(index, node.Scheduled().strftime("%Y-%m-%d") + "   " + node.Heading())
        if node.Scheduled() == today:
            todos_today.append(node.Scheduled().strftime("%Y-%m-%d") + "   " + node.Heading())

index, key = r.select('ORG-TODO', todos, message="Usage:", key1=('Alt+a', "Agenda for current week or day\n"), key2=('Alt+c', "Capture a new TODO entry"))
if key == 1:
    r.select('AGENDA-TODAY', todos_today, message="<b>   Date</b>" + "         " + "TODO")
elif key == 2:
    rofi_org_todo.todo_to_inbox(inbox_file)
