#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 help.py        Help information about the different commands.
 Author:        David @davlopgom / Rael Garcia <self@rael.io>
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

from __future__ import print_function

import os
import re
import sys
import json
from pybot.common.action import Action

HELP_FILE = os.path.join(os.path.dirname(__file__), "help.json")


def command_help(words):
    "Responds with information about a subject."

    command = re.search(r'.?(help)[\w\@]*\s*(\w*)\s*$', words, re.I | re.M)

    if command is None:
        return

    subject = command.group(2) or command.group(1)

    with open(HELP_FILE) as datafile:
        help_messages = json.load(datafile)

    if help_messages is None:
        return

    if subject in help_messages:
        return '\n'.join(help_messages[subject])

    return "No help available for subject _%s_" % subject


def help(message):
    "Implements hear to receive the messages and execute the plugin logic"
    return Action(
        name='new_message',
        target=message.chat.chat_id,
        text=command_help(message.text),
        markup='markdown'
    )


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(help(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
