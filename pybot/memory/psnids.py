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
import time
import re
import sys
import json
import io
from pybot.common.action import Action

PSNIDS_FILE = os.path.join(os.path.dirname(__file__), "psnids.json")


def __list_psnids(groupid):
    "Responds with information about a subject."

    with io.open(PSNIDS_FILE, "r", encoding="utf-8") as datafile:
        psnid_list = json.load(datafile)

    if psnid_list is None:
        return

    if str(groupid) in psnid_list:
        return '\n'.join(psnid_list[str(groupid)])

    return


def __escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def psnids(message):
    "Implements hear to receive the messages and execute the plugin logic"

    psnid_list = __list_psnids(message.chat.chat_id)

    if psnid_list:
        return Action(
            name='new_message',
            target=message.chat.chat_id,
            text=__escape_markdown(psnid_list),
            markup='markdown'
        )

    return


def main():
    "This allows to execute the plugin in standalone mode"
    if len(sys.argv) > 1:

        from pybot.common.message import Message
        from pybot.common.user import User
        from pybot.common.chat import Chat
        user = User(1, 'foo', 'bar', 'rael')
        chat = Chat(-1001082983975, 'Console', 'Console')
        message = Message(1, user, time.strftime,
                          ' '.join(sys.argv[1:]), chat, None)
        print(psnids(message))

    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
