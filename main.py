#!/bin/python3
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, print_json
from examples import custom_style_2
from pprint import pprint
import os
import subprocess


# This is python script to toggle DrawingTablet

def getdisplay():
    get_monitors = subprocess.Popen("xrandr --listmonitors", shell=True, stdout=subprocess.PIPE)
    monitors_list = get_monitors.stdout.readlines()
    displayList = []
    if len(monitors_list) > 0:
        monitors_list.pop(0)
        for x in monitors_list:
            # split by space and converting
            # string to list and
            displayname = str(x).split(" ")
            displayname = displayname[len(displayname) - 1].replace("\\n", '').replace("\'", '')
            displayList.append(displayname)
            # print(displayname)
        return displayList
    else:
        print('monitors list not found')
        exit()


def toggle(display_selected):
    print(display_selected)
    get_tablet = subprocess.Popen("xsetwacom --list", shell=True, stdout=subprocess.PIPE)
    the_tablet = get_tablet.stdout.read()
    the_tablet = str(the_tablet).replace("b'", '')
    the_tablet = the_tablet.split("\\n")

    pen_name = "na"
    pad_name = "na"
    cursor_name = "na"
    eraser_name = "na"

    for l in the_tablet:
        if "stylus" in str(l).lower():
            pen_name = l.split("\\t")[0].strip()
            print(pen_name)
            switch(pen_name, display_selected)
        if "pad" in str(l).lower():
            pad_name = l.split("\\t")[0].strip()
            print(pad_name)
            switch(pad_name, display_selected)
        if "cursor" in str(l).lower():
            cursor_name = l.split("\\t")[0].strip()
            switch(cursor_name, display_selected)
            print(cursor_name)
        if "eraser" in str(l).lower():
            eraser_name = l.split("\\t")[0].strip()
            switch(eraser_name, display_selected)
            print(eraser_name)

    # print(pen_name)
    # print(pad_name)
    # print(cursor_name)
    # print(eraser_name)


def switch(head, display):
    if display is None:
        print('Display set as None !!! returning ...')
        return 0
    cmd = 'xsetwacom set "' + head + '" MapToOutput ' + display
    os.system(cmd)
    print(cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    displayList = getdisplay()
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })
    questions = [
        {
            'type': 'list',
            'name': 'monitor_selected',
            'message': 'Which display you want to toggle?',
            'choices': displayList,
        },
    ]

    answers = prompt(questions, style=custom_style_2)
    toggle(answers.get("monitor_selected"))  # use the answers as input
