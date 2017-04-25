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
        media (str): Additional media attached to the message


    Args:
        message_id (int):
        user (:class:`pytbot.common.User`)
        chat (:class:`pytbot.common.Chat`)
        date (:class:`datetime.datetime`)
        text (str): Message text

    Keyword args:
        media (Optional[str]): Url of additional media attached to the message


    """

    def __init__(self,
                 message_id,
                 user,
                 date,
                 text,
                 chat,
                 media):

        # Required
        self.message_id = int(message_id)
        self.user = user
        self.date = date
        self.text = text
        self.chat = chat
        # Optionals
        self.media = media
