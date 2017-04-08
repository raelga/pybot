#!/usr/bin/env python
"""
 help.py        Help information about the different commands.
 Author:        David @davlopgom / Rael Garcia <self@rael.io>
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""
import os
import re
import sys
import json

HELP_FILE = os.path.dirname(__file__) +  "/help.json"

def command_help(words):
    "Responds with information about a subject."

    command = re.search(r'.?(help)\s*(\w*)\s*$', words, re.I|re.M)

    if command is None:
        return

    subject = command.group(2) or command.group(1)

    with open(HELP_FILE) as json_data:
        help_messages = json.load(json_data)

    if help_messages is None:
        return

    if help_messages.has_key(subject):
        return '\n'.join(help_messages[subject]).encode('utf-8')

    return "No help available for subject ", subject

def hear(words):
    "Implements hear to recieve the messages and forward them to the plugin logic"
    return command_help(words)

def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print hear(' '.join(sys.argv))
    else:
        print 'I heard nothing.'

if __name__ == "__main__":
    main(sys.argv)
