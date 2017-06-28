#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""

from __future__ import print_function

import os
import sys
import json
from pybot.common.action import Action

MENU_FILE = os.path.join(os.path.dirname(__file__), "menu.json")


class Menu(object):

    def __init__(self,
                 text):

        # Required
        self.text = text
        self.options = []

    def add_separator(self):
        "Adds a empty element to the menu."
        self.options.append([])

    def add(self, option_title, option_value):
        "Adds a new element to the menu."
        self.options.append([option_title, option_value])


def get_menu(menu_callback=None):
    "Returns the menu array from the MENU_FILE"

    with open(MENU_FILE, encoding='utf-8') as datafile:
        menu_data = json.load(datafile)

    if menu_data is None:
        return

    if menu_callback:

        for menu_name, menu_definition in menu_data.items():

            if menu_definition["callback"] == menu_callback:

                menu = Menu(menu_definition["text"])

                for option, value in menu_definition["options"].items():
                    menu.add(option, value)

                if menu.options:
                    menu.add_separator()
                    menu.add('< back', 'menu_main')
                    menu.add('x close', 'menu_exit')
                    return menu

    else:

        menu = Menu("Available menus.")
        for menu_name, menu_definition in menu_data.items():
            menu.add(menu_name, menu_definition["callback"])

        if menu.options:
            menu.add_separator()
            menu.add('x close', 'menu_exit')
            return menu

    return


def get_action(action, target, text=None, menu=None):
    "Return action class."

    if menu is not None:

        return Action(
            name=action,
            target=target,
            text=menu.text,
            markup="menu",
            payload=menu.options
        )

    elif text is not None:
        return Action(
            name=action,
            target=target,
            text=text
        )

    return


def menu_main(message):
    "Retuns the available menus."

    return get_action(
        action="edit_message",
        target=message.message_id,
        menu=get_menu()
    )


def menu_pkts(message):
    "Returns the Groups menu."

    return get_action(
        action="edit_message",
        target=message.message_id,
        menu=get_menu('menu_pkts')
    )

def menu_meristation(message):
    "Returns the Meristation menu."

    return get_action(
        action="edit_message",
        target=message.message_id,
        menu=get_menu('menu_meristation')
    )

def menu_exit(message):
    "Closes the menu."

    return get_action(
        action="edit_message",
        target=message.message_id,
        text="🙊"
    )


def menu_list(message):
    "Return the main menu for the command `show_menu`."

    return get_action(
        action="new_message",
        target=message.message_id,
        menu=get_menu()
    )


def groups(message):
    "Returns the groups menu for the command shortcut `groups`."

    return get_action(
        action="new_message",
        target=message.message_id,
        menu=get_menu('menu_pkts')
    )


def meristation(message):
    "Returns the groups menu for the command shortcut `groups`."

    return get_action(
        action="new_message",
        target=message.message_id,
        menu=get_menu('menu_meristation')
    )

def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(show_menu(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
