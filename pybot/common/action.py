#!/usr/bin/env python

"This module contains an object that represents an action."


class Action(object):
    """This  objectes represents a action.

    Use :class:`Action` methods to get instances of this class.

    Attributes:
        name (int):
        target (str):
        text (str):
        markup (str):
        payload (dict):

    Args:
        name (int):
        target (str):
        text (str):

    Keyword Args:
        markup (Optional[dict]):
        payload (Optional[dict]):

    """

    def __init__(self,
                 name,
                 target,
                 text,
                 markup=None,
                 payload=None):

        # Required
        self.name = name
        self.target = target
        self.text = text
        # Optionals
        self.markup = markup
        self.payload = payload

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)
