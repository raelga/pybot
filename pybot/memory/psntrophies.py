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
    gold = 0
    silver = 0
    bronze = 0
    completed = 0
    info = "Recent games played:\n\n"

    for game in range(games):
        if game <= 5:
            info += "👾  " + data['list'][game]['title'] + \
                " (" + repr(data['list'][game]['progress']) + "%)\n"
        if data['list'][game]['progress'] == 100:
            completed += 1

        platinum += data['list'][game]['trophies']['platinum']
        gold += data['list'][game]['trophies']['gold']
        silver += data['list'][game]['trophies']['silver']
        bronze += data['list'][game]['trophies']['bronze']

    if not games:
        info = "No games available, check the %s privacy settings."
    else:
        level = data['curLevel']
        points = platinum * 180 + gold * 90 * silver * 30 + bronze * 15

        summary = '\n'.join(
            [
                "*%s*" % (psnid),
                "%s platinums (%s 100%%s)" % (platinum, completed),
                "",
                "🥇 %s 🥈 %s 🥉 %s" % (gold, silver, bronze),
                "⭐️ %s - %s points" % (level, points)
            ]
        )

    return summary + "\n\n" + info


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
