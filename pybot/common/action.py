#!/usr/bin/env python

"This module contains an object that represents an action."


class Action(object):
    """This  object represents an action.

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
                 target=None,
                 text=None,
                 markup=None,
                 payload=None):

        # Required
        self.name = name
        # Optionals
        self.target = target
        self.text = text
        self.markup = markup
        self.payload = payload

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)
