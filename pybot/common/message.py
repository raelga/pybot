#!/usr/bin/env python

"This module contains an object that represents a message."


class Message(object):
    """This  objectes represents a person.

    Use :class:`Person` methods to get instances of this class.


    Attributes:
        message_id (int): Message identifier
        user (:class:`pytbot.common.User`): User who sent the message
        chat (:class:`pytbot.common.Chat`): Chat where the message was posted
        date (:class:`datetime.datetime`): Timestamp of the message
        text (str): Message text


    Args:
        person_id (int):
        first_name (str):

    """

    def __init__(self,
                 message_id,
                 user,
                 date,
                 text,
                 chat):

        # Required
        self.message_id = int(message_id)
        self.user = user
        self.date = date
        self.text = text
        self.chat = chat
