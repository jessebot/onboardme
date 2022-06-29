#!/usr/bin/env python3
from datetime import date

agenda_line = "Today's Agenda"
today = date.today
today_pretty = today.strftime("%d-%m-%Y")

def update_yesterday_and_today(line):
    """
    """





def is_today():
    """
    takes two dates and compares them
    """
    if



with open('~/todo.md') as todo_file:
    for line in todo_file.readlines():
        if agenda_line in line:
            time = line.split(':')
            if is_today()

