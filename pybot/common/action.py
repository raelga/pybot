#!/usr/bin/env python

"This module contains an object that represents a action."


class Action(object):
    """This  objectes represents a action.

    Use :class:`Action` methods to get instances of this class.

    Attributes:
        name (int):
        target (str):
        text (str):
        payload_type (str):
        payload (dict):

    Args:
        name (int):
        target (str):
        text (str):

    Keyword Args:
        payload_type (Optional[dict]):
        payload (Optional[dict]):

    """

    def __init__(self,
                 name,
                 target,
                 text,
                 payload_type=None,
                 payload=None):

        # Required
        self.name = name
        self.target = target
        self.text = text
        # Optionals
        self.payload_type = payload_type
        self.payload = payload
