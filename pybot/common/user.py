#!/usr/bin/env python

"This module contains an object that represents an entity."


class User(object):
    """This  objectes represents an entity: user, bot or something.

    Use :class:`Entity` methods to get instances of this class.

    Attributes:
        user_id (int):
        first_name (str):
        last_name (str):
        username (str):
        specie (str):
        photo (srt):

    Args:
        user_id (int):
        first_name (str):

    Keyword Args:
        last_name (Optional[str]):
        username (Optional[str]):
        specie (Optional[str]):
        photo (Optional[str]):
    """

    def __init__(self,
                 user_id,
                 first_name,
                 last_name=None,
                 username=None,
                 specie=None,
                 photo=None):

        # Required
        self.user_id = int(user_id)
        self.first_name = first_name
        # Optionals
        self.specie = specie
        self.last_name = last_name
        self.username = username
        self.photo = photo

    @property
    def name(self):
        """str: """
        if self.username:
            return '@%s' % self.username
        if self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.first_name
