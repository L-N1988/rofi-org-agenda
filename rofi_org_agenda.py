import orgparse
import rofi_org_todo
import datetime as dt
from rofi import Rofi
import bisect

def mark_done(file, linenumber):
    # readlines begins with 0 instead of 1
    linenumber -= 1
    # Open file for both reading and writing (mode 'r+')
    with open(file, 'r+') as f:
        # Read all lines into a list
        lines = f.readlines()
        # Insert new line at index 2 (line numbers start from 0)
        print(lines[linenumber])
        lines[linenumber] = lines[linenumber].replace("TODO", "DONE")
        print(lines[linenumber])
        # Move file pointer to beginning of file
        f.seek(0)
        # Write modified lines back to the file
        f.writelines(lines)
    return 

# change this to align output strings
MAX_LINE_CHAR = 55 # approx max chars number in one line of rofi

# path to where you want your TODOs to be inserted to
inbox_file = "/home/liuning/org/TODO.org"
r = Rofi()
root = orgparse.load(inbox_file)
today = dt.date.today()

todos = []
todos_today = []
sch_list = []
child_linenums = []
child_today_linenums = []
for child in root.children:
    if child.todo == 'TODO':
        if child.scheduled.start is None:
            # Not scheduled entries are appended to last
            todos.append(child.heading)
            child_linenums.append(child.linenumber)
        else:
            # Find the index where the new item should be inserted
            i_node = bisect.bisect(sch_list, child.scheduled.start)
            # Insert the new item into the list at the correct position
            sch_list.insert(i_node, child.scheduled.start)
            child_linenums.insert(i_node, child.linenumber)
            todos.insert(i_node, child.scheduled.start.strftime("%Y-%m-%d %a") + "   " + child.heading)
        if child.scheduled.start == today:
            todos_today.append(child.scheduled.start.strftime("%Y-%m-%d %a") + "   " + child.heading)
            child_today_linenums.append(child.linenumber)

i_all, key = r.select('ORG-TODO', todos, message="Usage:", \
    key1=('Alt+a', "Agenda for current week or day.\n"), \
        key2=('Alt+c', "Capture a new TODO entry.\n"), \
            key3=('Ctrl+t', "Mark done TODO entry."))
if key == 1:
    i_today, k_today = r.select('AGENDA-TODAY', todos_today, message="<b>   Date</b>" + "             " + "TODO", \
        key1=('Alt+a', "Return agenda for all.\n"), \
            key2=('Alt+c', "Capture a new TODO entry.\n"), \
                key3=('Ctrl+t', "Mark done TODO entry."))
    if k_today == 1:
        r.select('ORG-TODO', todos)
    elif k_today == 2:
        rofi_org_todo.todo_to_inbox(inbox_file)
    elif k_today == 3:
        mark_done(inbox_file, child_today_linenums[i_today])

elif key == 2:
    rofi_org_todo.todo_to_inbox(inbox_file)
elif key == 3:
    mark_done(inbox_file, child_linenums[i_all])
