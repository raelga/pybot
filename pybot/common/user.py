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
        photo (srt):
        bio (srt):
        human (bool):

    Args:
        user_id (int):
        first_name (str):

    Keyword Args:
        last_name (Optional[str]):
        username (Optional[str]):
        photo (Optional[str]):
        human (Optional[bool]):
    """

    def __init__(self,
                 user_id,
                 first_name,
                 last_name=None,
                 username=None,
                 photo=None,
                 bio=None,
                 human=None):

        # Required
        self.user_id = int(user_id)
        self.first_name = first_name
        # Optionals
        self.last_name = last_name
        self.username = username
        self.photo = photo
        self.bio = bio
        self.human = human

    @property
    def name(self):
        """str: """
        if self.username:
            return '@%s' % self.username
        if self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.first_name

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)
