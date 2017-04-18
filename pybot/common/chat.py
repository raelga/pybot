#!/usr/bin/env python

"This module contains an object that represents a chat."


class Chat(object):
    """This  objectes represents a chat.

    Use :class:`Chat` methods to get instances of this class.

    Attributes:
        chat_id (int):
        chat_type (str):
        chat_name (str):

    Args:
        chat_id (int):
        chat_type (str):

    Keyword Args:
        chat_name (Optional[str]):

    """

    def __init__(self,
                 chat_id,
                 chat_type,
                 chat_name=None):

        # Required
        self.chat_id = int(chat_id)
        self.chat_type = chat_type
        # Optionals
        self.chat_name = chat_name
