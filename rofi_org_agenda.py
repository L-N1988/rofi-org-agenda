import orgparse
import Orgmode
import rofi_org_todo
import datetime as dt
from rofi import Rofi

MAX_LINE_CHAR = 65

# path to where you want your TODOs to be inserted to
inbox_file = "/home/liuning/org/TODO.org"
r = Rofi()
nodes = Orgmode.makelist(inbox_file)
today = dt.date.today()

todos = []
todos_today = []
for node in nodes:
    if node.Todo() == 'TODO':
        n_space = MAX_LINE_CHAR - len(node.Heading() + str(node.Scheduled()))
        todos.append(node.Heading() + " "*n_space + str(node.Scheduled()))
        if node.Scheduled() == today:
            todos_today.append(node.Heading() + " "*n_space + str(node.Scheduled()))

index, key = r.select('ORG-TODO', todos, message="Usage:", \
    key1=('Alt+a', "Agenda for current week or day\n"), \
        key2=('Alt+c', "Capture a new TODO entry"))
if key == 1:
    n_space = MAX_LINE_CHAR - len("   TODO" + "Date") - 3 # FIXME: tedious format output to align all items
    r.select('AGENDA-TODAY', todos_today, message="<b>   TODO</b>" + " "*n_space + "Date")
elif key == 2:
    rofi_org_todo.todo_to_inbox(inbox_file)
