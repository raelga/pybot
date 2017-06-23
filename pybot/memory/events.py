#!/usr/bin/env python
"""
 rael.py        Responses for user events.
 Author:        Rael Garcia <self@rael.io>
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

import os
import time
import sys
import json
import io
from pybot.common.action import Action


EVENTS_FILE = os.path.join(os.path.dirname(__file__), "events.json")


def __get_message(event, message):
    "Responds with information about a subject."

    with io.open(EVENTS_FILE, "r", encoding="utf-8") as datafile:
        events_json = json.load(datafile)

    if events_json is None:
        return

    if event in events_json:
        if str(message.chat.chat_id) in events_json[event]:
            text = '\n'.join(events_json[event][str(message.chat.chat_id)])
            text = text.replace('#-#username#-#', message.user.name)
            text = text.replace('#-#groupname#-#',
                                "*" + message.chat.chat_name + "*")
            if text:
                return text

    return


def user_entering(message):
    "Response to user entering a group events."

    custom_message = __get_message(
        'user_entering',
        message
    )

    if custom_message:
        return Action(
            name='new_message',
            target=message.chat.chat_id,
            text=custom_message,
            markup='markdown'
        )

    return "👋"


def user_leaving(message):
    "Response to user leaving a group events."

    custom_message = __get_message(
        'user_leaving',
        message
    )

    if custom_message:
        return Action(
            name='new_message',
            target=message.chat.chat_id,
            text=custom_message,
            markup='markdown'
        )

    return "👋👋"


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
        print(user_entering(message))
        print(user_leaving(message))

    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main()
