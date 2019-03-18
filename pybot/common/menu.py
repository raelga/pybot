#!/usr/bin/env python

"This module contains an object that represents a message."


class Menu(object):
    """This  objectes represents a person.

    Use :class:`Person` methods to get instances of this class.


    Attributes:
        message_id (int): Message identifier
        user (:class:`pytbot.common.User`): User who sent the message
        chat (:class:`pytbot.common.Chat`): Chat where the message was posted
        date (:class:`datetime.datetime`): Timestamp of the message
        text (str): Message text
        media (str): Additional media attached to the message
        menu (dict): Additional menu attached to the message

    Args:
        message_id (int):
        user (:class:`pytbot.common.User`)
        chat (:class:`pytbot.common.Chat`)
        date (:class:`datetime.datetime`)
        text (str): Message text

    """

    def __init__(self,
                 menu_id,
                 name,
                 text,
                 callback,
                 options):

        # Required
        self.menu_id = int(menu_id)
        self.name = name
        self.text = text
        self.callback = callback
        self.options = options

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)

    def add_separator(self):
        "Adds a empty element to the menu."
        self.options.append([])

    def add(self, option_title, option_value):
        "Adds a new element to the menu."
        self.options.append([option_title, option_value])