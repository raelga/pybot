#!/usr/bin/env python
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          09/2021
 Tested on:     Python 3 / OS X 10.11.5
"""
import logging
import requests
import sys
from pybot.common.action import Action

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOG = logging.getLogger(__name__)


def __cas_banned(user_id):
    cas_api_endpoint = 'https://api.cas.chat/check?'
    qstr = {'user_id': user_id}

    try:
        resp = requests.get(cas_api_endpoint, params=qstr, timeout=2)

    except requests.exceptions.Timeout as err:
        LOG.warning("Timeout while CAS API infor for %s. (%s)", user_id, err)

    return False


def __dubious_bio():
    return False


def ban_user(user_id, info):
    "Returns ban_user action when the user is targeted for a ban."

    return Action(
        name="ban_user",
        target=user_id,
        text=info
    )

    return None


def user_entering(message):
    "Response to user entering a group events."
    return None


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


    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main()
