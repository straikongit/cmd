#!/usr/bin/python

import re
import json
import sys
import os
from  pprint import pprint
import readline
import re
import pyperclip
import reprlib

from classes import kindaDB
from classes import color

#from clint import colors
#from termcolor import colored
#import pickle


def globalVars():
    global activeCommand
    activeCommand = None

def runAction(actionMap):
    action=actionMap[0]
    if action.isdigit():
        cmdSelect(int(action))
    elif action   == "copy" or action == "c":
        if len(actionMap) > 1:
            cmdCopy(actionMap[1])
    elif action ==  "run":
        cmdRun()
    elif action ==  "help" or action == "h":
        cmdHelp()
    elif action ==  "options":
        cmdOptions()
    elif action ==  "set":
        if len(actionMap) == 3:
            cmdSet(actionMap[1],actionMap[2])
        else:
            print("usage : set [option] [value]")
    elif action ==  "global":
        if len(actionMap) == 3:
            cmdGlobal(actionMap[1],actionMap[2])
        else:
            print("usage : global [option] [value]")
    elif action ==  "search" or action == "s":
        if len(actionMap) > 1:
            cmdSearch(actionMap[1:])
    elif action ==  "save":
            cmdSaveOptions(actionMap[1:])
    elif action ==  "load":
            cmdLoadOptions(actionMap[1:])
    elif action ==  "q":
        exit(1)
    else:
        print("command not found")
    	
def cmdHelp():
    print("""
    
    available commands:
    
    help | h        			-->     show this help
    [number]     			-->     select and load command with ID = number
    c [number]    			-->     copies selected command to clipboard
    options      			-->     shows msf-style options
    set          			-->     set [option] [value]
    global          			-->     set [option] [value]
    search | s [string] ... [-][string] -->     search commands, the [-] excludes [string] from results
    q            			-->     end program

    """)

def cmdSelect(ID):
    global activeCommand
    cmd=db.getCommand(ID)
    if cmd:
        activeCommand=ID
        printCommand(ID)
        #print "command " + ID + " selected"
        #cmdOptions()
    else:
        print("command " + ID + " not found")

def cmdOptions():
    global activeCommand
    if not activeCommand:
        print("no active command")
    else:
        ID = activeCommand 
        options = db.getOptions(ID)
        for option in options:
            if options[option]:
                print("    " + option + "           -->      " + options[option]) 
            else:
                print("    " + option + "           -->      " + "not set") 
    print("global options:")
    options = db.getGlobalOptions()
    if len(options):
        for option in options:
            if options[option]:
                print("    " + option + "           -->      " + options[option]) 
    else:
        print("not set")

    print(" ")

def cmdSet(option ,value):
    global activeCommand
    if not activeCommand:
        print("no active command")
        return
    db.setOptions(activeCommand,option,value)
    cmdOptions()

def cmdSaveOptions(actionMap):
    if len(actionMap) :
        fname = actionMap[0]
    else:
        fname = os.path.join(sys.path[0], "options.json")
    db.saveOptions(fname)

def cmdLoadOptions(actionMap):
    if len(actionMap):
        fname = actionMap[0]
        if not os.path.isfile(fname) :
            print("file " + fname + " not found") 
            return
    else:
        fname = os.path.join(sys.path[0], "options.json")
    db.LoadOptions(fname)


def cmdGlobal(option ,value):
    db.setGlobalOptions(option,value)
    print("    " + option + "           -->      " + value) 
    cmdOptions()

def cmdCopy(ID):

    cmd=db.getCommand(ID)
    if cmd:
        cbytes = db.getModifiedCommand(ID,colored = False).encode('ascii','ignore')
        s = cbytes.decode("utf-8")
        #pyperclip.copy(db.getModifiedCommand(ID,colored = False).encode('ascii','ignore'))
        pyperclip.copy(s)
        print("command " + ID + " copied to clipboard \n ")
    else:
        print("command " + ID + " not found")
def cmdRun():
    print("cmdRun")
    show()

def cmdSearch(searchTerm):
    print("""

matching commands
=================

    """)
    for ID in db.search(searchTerm):
        printCommand(ID,True)
    print("""
""")

def printCommand(ID,fold = False):

    cmd = db.getCommand(ID)
    
    if cmd:
        print((color.BLUE + '[{0}] ' \
                + color.LIGHTBLUE + '{1} ' \
                + color.END).format(cmd['id'], \
                cmd['header']))

        s = db.getModifiedCommand(ID)
        if fold:
            arr = s.split("\r")
            if len(arr)>4:
                s= "\r".join(arr[0:4]) \
                + "\r\n" + color.RED + "..." + color.END
        print(s)
        print(' ')
    

db= kindaDB

def main(argv):
    globalVars()
    global db
    db = kindaDB(os.path.dirname(os.path.realpath(__file__)) +'/cmd.json')
    if len(argv) > 1:
        if argv[1] == "-h" or argv[1] == "--help":
            print("python cmd.py [SEARCHTERM]")
            print("to get more help use 'help' from inside the Program")
            exit(0)
        else:
            action =   argv
            action[0] = "search"
            runAction(action)
    while True:
        #readline.parse_and_bind('tab: complete')
        #readline.parse_and_bind('set editing-mode vi')
        #action = readline.get_line_buffer().split()
        action = input(":").split()
        if len(action) >0:
            runAction(action)

if __name__ == "__main__":
    main(sys.argv)
    
    






