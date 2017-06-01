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
import re
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

    platinum = 0
    gold = 0
    silver = 0
    bronze = 0
    completed = 0
    games = []

    for game in range(len(data['list'])):
        if game <= 5:

            info = "👾  " + __escape_markdown(data['list'][game]['title']) + " - _"

            if data['list'][game]['trophies']['platinum']:
                info += "🏆 with "

            info += repr(data['list'][game]['progress']) + "%_"

            games.append(info)

        if data['list'][game]['progress'] == 100:
            completed += 1

        platinum += data['list'][game]['trophies']['platinum']
        gold += data['list'][game]['trophies']['gold']
        silver += data['list'][game]['trophies']['silver']
        bronze += data['list'][game]['trophies']['bronze']

    if not games:
        return "No information available for *" + psnid + "*, " + \
            "check the user privacy settings."
    else:
        level = data['curLevel']

        summary = [
            "*%s* ⭐️ *%s* - _%s trophies_" %
            (psnid, level, platinum + gold + silver + bronze),
            "",
            "🏆 %s platinums (%s 100%%s)" % (platinum, completed),
            "_     🥇 %s 🥈 %s 🥉 %s_" % (gold, silver, bronze)
        ]

    return '\n'.join(
        summary +
        ["", "Recent games played", ""] +
        games
    )

def __escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

def __usage(handler):
    """Prints usage information with the handler command."""
    return (
        'Usage: *%s* _PSNID_'
        % (handler)
    )


def ___message_handler(message):
    """Parses the user message call the psnprofiles method if valid"""

    words = message.text.split()

    if not words:
        return None

    handler = words[0]

    if len(words) < 2:
        response = __usage(handler)
    else:
        response = __psntrophies(words[1])

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


def main():
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
