#!/bin/python3
import sys
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
from rofi import Rofi

def todo_to_inbox(inbox_file):
    r = Rofi()
    todo = r.text_entry("TODO", message="""Usage: 
    Type full text of org TODO and schedule time in format:
    1. +number d/w/m/y
    2. month-day
    3. default schedule for today
    eg. Code rofi-org-todo for fast adds to inbox +1w
    """)
    if todo is not None:
        ender = todo.split()[-1]
        # case 1: to schedule for relative date 
        if ender[0] == '+' and ender[-1] in ['d', 'w', 'm', 'y']:
            if ender[-1] == 'd':
                sch_time = dt.datetime.now() + relativedelta(days=+int(ender[1:-1]))
            elif ender[-1] == 'w':
                sch_time = dt.datetime.now() + relativedelta(weeks=+int(ender[1:-1]))
            elif ender[-1] == 'm':
                sch_time = dt.datetime.now() + relativedelta(months=+int(ender[1:-1]))
            else:
                sch_time = dt.datetime.now() + relativedelta(years=+int(ender[1:-1]))
            todo = " ".join(todo.split()[0:-1])          
        # case 2: to schedule for absolute date 
        elif len(ender.split("-")) == 2:
            month_str, day_str = ender.split("-")
            month = int(month_str)
            day = int(day_str)
            try:
                sch_time = dt.date(dt.date.today().year, month, day)
                todo = " ".join(todo.split()[0:-1])
            except ValueError:
                print("Invalid month or day")
                sch_time = dt.date.today()
        # case 3: to schedule for today 
        else:
            sch_time = dt.date.today()
        f = open(inbox_file, "a")
        f.write("\n* TODO ")
        f.write(todo + "\n")
        f.write("SCHEDULED: " + "<" + sch_time.strftime("%Y-%m-%d %a") + ">\n")
        f.write(":PROPERTIES:\n")
        f.write(":CREATED: " + "[" + dt.datetime.now().strftime("%Y-%m-%d %a %H:%M") + "]\n")
        f.write(":END:\n")
        f.close()
