#!/usr/bin/env python
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys
import random


def send_a_cat(message):
    "Get a random cat from catapi"

    cat_apiurl = "http://thecatapi.com/api/images/get?format=src&type=gif"
    cat_users = [329350632, 53693428, 13932196]

    if message.user.user_id in cat_users:
        if re.search(r'(^|\s)g[aA0-9]t.', message.text, re.I | re.M) \
                or re.search(r'\\U0001F63[8-9A-F]', message.text, re.I | re.M) \
                or re.search(r'(🐈|🐱|😺|😸|😹|😻|😼|😽|🙀|😿|😾)',
                             message.text, re.I | re.M):
            return cat_apiurl + "&timestamp=" + \
                str(random.random()) + ".gif"


def interact(message):
    "Implements hear to receive the messages and execute the plugin logic"
    return send_a_cat(message)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
