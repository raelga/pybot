#!/usr/bin/env python
"""
 psnthropies.py List PSN trohpies information from a PSN ID.
 Author:        Rael Garcia <self@rael.io>
 Date:          01/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

from urllib import request as r
import json
import sys
import time
from pybot.common.action import Action


def __psntrophies(psnid):

    url = "https://io.playstation.com/playstation/psn/public/trophies/?onlineId="
    headers = {"Referer": "https://www.playstation.com/en-us/my/compare-game-trophies",
               "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}

    req = r.Request(url + psnid, None, headers)
    resp = r.urlopen(req)
    body = resp.read()
    encoding = resp.info().get_content_charset('utf-8')
    data = json.loads(body.decode(encoding))

    games = len(data['list'])
    platinum = 0
    completed = 0
    info = "Recent games played:\n\n"

    for g in range(games):
        if g <= 5:
            info += "👾  " + data['list'][g]['title'] + \
                " (" + repr(data['list'][g]['progress']) + "%)\n"
        if data['list'][g]['progress'] == 100:
            completed += 1
        if data['list'][g]['trophies']['platinum'] == 1:
            platinum += 1

    summary = "*" + psnid + "*\n" + repr(platinum) + \
        " platinums (" + repr(completed) + " 100%s)"

    return summary + "\n\n" + info


def __usage(handler):
    """Prints usage information with the handler command."""
    return (
        'Usage: *%s* _PSNID_'
        % (handler)
    )


def __mdsafe(text):
    """Escape unsafe Markdown characters."""
    return text.replace("_", r"\_")


def ___message_handler(message):
    """Parses the user message call the psnprofiles method if valid"""

    words = message.text.split()

    if not words:
        return None

    handler = words[0]

    if len(words) < 2:
        response = __usage(handler)
    else:
        response = __mdsafe(__psntrophies(words[1]))

    return Action(
        name='new_message',
        target=message.chat.chat_id,
        text=response,
        markup='markdown'
    )


def perfil(message):
    "This allows to respond to /perfil command."
    return ___message_handler(message)


def trophies(message):
    "This allows to respond to /trohpies command."
    return ___message_handler(message)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(sys.argv) > 1:

        from pybot.common.message import Message
        from pybot.common.user import User
        from pybot.common.chat import Chat
        user = User(1, 'foo', 'bar', 'rael')
        chat = Chat(1, 'Console', 'Console')
        message = Message(1, user, time.strftime,
                          ' '.join(sys.argv[1:]), chat, None)
        print(trophies(message))

    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
