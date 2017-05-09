#!/usr/bin/env python
# pylint: disable=I0011,R0903,R0913
# -*- coding: utf-8 -*-
"""
 fireteams.py   Help information about the different commands.
 Author:        David @davlopgom
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

import time
import os
import re
import sys
import sqlite3
import dateparser
from pybot.common.action import Action

DB_FILE = os.path.join(os.path.dirname(__file__), "fireteams.sqlite")
VALID_ACTIONS = ['new', 'view', 'join', 'leave', 'check']


class FireteamsCmd(object):
    """Represent an fireteams command definition."""

    def __init__(self,
                 handler,
                 action,
                 chat_id,
                 user_id,
                 activity=None,
                 username=None):

        # Required
        self.handler = handler
        self.action = action
        self.chat_id = chat_id
        self.user_id = user_id
        self.activity = activity
        self.username = username

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)


class Activity(object):
    """Represent an activity definition."""

    def __init__(self,
                 date,
                 hour,
                 name,
                 description):

        # Required
        self.date = date
        self.hour = hour
        self.name = name
        self.description = description

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)


#
# Fireteams actions
#


def __fireteams_check():
    """"Initialize the database, creating the tables if missing."""

    return __initialize_database()


def __fireteams_view(chat_id, activity):
    """"Method to list activities."""

    activities = __db_select('activity_id, date, hour, name, description',
                             'activities', chat_id, name=activity.name,
                             date=activity.date, hour=activity.hour,
                             order='date, hour, name')

    if not activities and activity.hour:
        return ('No activities available for %s at %s.'
                % (activity.date, activity.hour))

    if not activities:
        return ('No activities available for %s.'
                % (activity.date))

    output = []

    output.append('#\n# Activities\n#')
    output.append('')

    for act in activities:

        output.append('*%s %s %s*' %
                      (act[1], act[2], __escape_markdown(act[3])))

        if act[4]:
            output.append('_%s_' % (__escape_markdown(act[4])))

        output.append('-')

        fireteams = __db_select('username', 'fireteams',
                                chat_id, activity_id=act[0], order='timestamp')
        if fireteams:
            pos = 1
            for fireteam in fireteams:
                output.append('*%d* - %s' %
                              (pos, __escape_markdown(fireteam[0])))
                pos = pos + 1
        else:
            output.append('_Nobody_')

        output.append('')

    return '\n'.join(output)


def __fireteams_new(chat_id, user_id, activity):
    """Method create a new empty activity"""

    if not activity.date \
            or not activity.hour \
            or not activity.name:
        return 'You must provide date, time and name for the activity.'

    if __get_activity_id(chat_id, activity):
        return ('Activity _%s %s %s_ already exists.'
                % (activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    if __store_activity(chat_id, user_id, activity):
        return ('Activity _%s %s %s_ added.'
                % (activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    return 'Unable to create the new activity.'


def __fireteams_join(chat_id, user_id, activity, username):
    """Method to add players to a fireteam."""

    if not activity.date \
            or not activity.hour \
            or not activity.name:
        return 'You must provide date, time and name for the activity.'

    activity_id = __get_activity_id(chat_id, activity)

    if not activity_id:
        return ('Activity _%s %s %s_ does not exists.'
                % (activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    if __check_activity_user(chat_id, user_id, activity_id):
        return ('%s already joined to _%s %s %s_.'
                % (__escape_markdown(username),
                   activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    if __store_player(chat_id, user_id, username, activity_id):
        return ('%s joined _%s %s %s_ fireteam.'
                % (__escape_markdown(username),
                   activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    return 'Unable to add the user to the activity.'


def __fireteams_leave(chat_id, user_id, activity, username):
    """Method to remove players from a fireteam."""

    activity_id = __get_activity_id(chat_id, activity)

    if not activity.date \
            or not activity.hour \
            or not activity.name:
        return 'You must provide date, time and name for the activity.'

    if not activity_id:
        return ('Activity _%s %s %s_ does not exists.'
                % (activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    if not __check_activity_user(chat_id, user_id, activity_id):
        return ('%s not a member of _%s %s %s_.'
                % (__escape_markdown(username),
                   activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    if __remove_player(chat_id, user_id, activity_id):
        return ('%s left _%s %s %s_ fireteam.'
                % (__escape_markdown(username),
                   activity.date, activity.hour,
                   __escape_markdown(activity.name)))

    return 'Unable to remove the user from the activity.'


def __fireteams_do(cmd):
    """Method to dispatch the fireteams commands."""

    if cmd.action == 'check':

        return __fireteams_check()

    if cmd.action == 'view':

        return __fireteams_view(cmd.chat_id, cmd.activity)

    if cmd.action == 'new':

        return __fireteams_new(cmd.chat_id,
                               cmd.user_id,
                               cmd.activity)

    if cmd.action == 'join':

        return __fireteams_join(cmd.chat_id,
                                cmd.user_id,
                                cmd.activity,
                                cmd.username)

    if cmd.action == 'leave':

        return __fireteams_leave(cmd.chat_id,
                                 cmd.user_id,
                                 cmd.activity,
                                 cmd.username)

    return None

#
# DB Helpers
#


def __initialize_database():
    """Create the database file and tables."""
    if __db_init():
        return 'Database OK.'
    else:
        return 'Database KO.'


def __store_activity(chat_id, user_id, activity):
    """Store the activity in the database."""

    dbh = __db_handler()
    stored = False

    try:
        cursor = dbh.cursor()
        cursor.execute(
            'INSERT INTO activities'
            '(chat_id, user_id, name, description, date, hour)'
            'VALUES'
            '(?,?,?,?,?,?);',
            (chat_id, user_id, activity.name,
             activity.description, activity.date, activity.hour)
        )

        dbh.commit()

        stored = True

    except sqlite3.Error as err:
        dbh.rollback()
        print('SQLite error: %s' % (' '.join(err.args)))

    dbh.close()
    return stored


def __store_player(chat_id, user_id, username, activity_id):
    """Store the username in the database."""

    dbh = __db_handler()
    stored = False

    try:
        cursor = dbh.cursor()
        cursor.execute(
            'INSERT INTO fireteams'
            '(chat_id, user_id, activity_id, username)'
            'VALUES'
            '(?,?,?,?);',
            (chat_id, user_id, activity_id, username)
        )

        dbh.commit()

        stored = True

    except sqlite3.Error as err:
        dbh.rollback()
        print('SQLite error: %s' % (' '.join(err.args)))

    dbh.close()
    return stored


def __remove_player(chat_id, user_id, activity_id):
    """Store the username in the database."""

    dbh = __db_handler()
    removed = False

    try:
        cursor = dbh.cursor()
        cursor.execute(
            'DELETE FROM fireteams '
            'WHERE chat_id = ? '
            'AND user_id = ? '
            'AND activity_id = ? ',
            (chat_id, user_id, activity_id)
        )

        dbh.commit()

        removed = True

    except sqlite3.Error as err:
        dbh.rollback()
        print('SQLite error: %s' % (' '.join(err.args)))

    dbh.close()
    return removed


def __get_activity_id(chat_id, activity):
    """Retrieves, if exists in the database, the activity id for activity."""

    activity_id = __db_select(
        'activity_id', 'activities',
        chat_id, name=activity.name,
        date=activity.date, hour=activity.hour
    )

    if activity_id:
        return activity_id[0][0]

    return None


def __check_activity_user(chat_id, user_id, activity_id):
    """Retrieves, if exists in the database, the activity id for activity."""

    return __db_select(
        'user_id', 'fireteams',
        chat_id, user_id=user_id, activity_id=activity_id
    )


def __db_handler():
    """Method to create the DB connection."""

    try:
        return sqlite3.connect(DB_FILE)
    except sqlite3.Error:
        pass

    return None


def __db_init():
    """Method to create the init DB and table if doesn't exists"""

    dbh = __db_handler()
    initialized = False

    if dbh:

        try:
            cursor = dbh.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS activities('
                'activity_id INTEGER, '
                'chat_id INTEGER NOT NULL, '
                'user_id INTEGER NOT NULL, '
                'name TEXT NOT NULL, '
                'description TEXT, '
                'date TEXT NOT NULL, '
                'hour TEXT NOT NULL, '
                'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, '
                'UNIQUE(chat_id, date, hour, name), '
                'PRIMARY KEY(activity_id ASC)'
                ');'
            )

            cursor.execute(
                'CREATE TABLE IF NOT EXISTS fireteams('
                'fireteams_id INTEGER NOT NULL, '
                'activity_id INTEGER NOT NULL, '
                'chat_id INTEGER NOT NULL, '
                'user_id INTEGER NOT NULL, '
                'username TEXT NOT NULL, '
                'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, '
                'UNIQUE (activity_id, chat_id, user_id), '
                'PRIMARY KEY(fireteams_id ASC)'
                ');'
            )

            dbh.commit()

            initialized = True

        except sqlite3.Error as err:
            dbh.rollback()
            print('SQLite error: %s' % (' '.join(err.args)))

        dbh.close()

        return initialized


def __db_select(what, table, chat_id, order=None, **kwargs):
    """Execute a select query with the arguments provided."""

    sql = []
    where = []
    values = []

    sql.append('SELECT %s' % what)
    sql.append('FROM %s' % table)

    where.append("WHERE chat_id = ?")
    values.append(chat_id)

    for column, value in kwargs.items():
        if value:
            where.append("%s = ?" % column)
            values.append(value)

    if where:
        sql.append(' AND '.join(where))

    if order:
        sql.append('ORDER BY %s' % order)

    return __db_execute_sql(' '.join(sql), values)


def __db_execute_sql(query, values):
    """Returns a recordset with the result of the sql query."""

    dbh = __db_handler()
    recordset = None

    if dbh:
        try:
            cursor = dbh.cursor()
            cursor.execute(query, values)
            recordset = cursor.fetchall()
            dbh.commit()

        except sqlite3.Error as err:
            dbh.rollback()
            print('SQLite error: %s' % (' '.join(err.args)))

    dbh.close()

    return recordset


#
# Parsers
#


def __parse_date(date):
    """Method to parse the date to an common format"""

    try:
        return dateparser.parse(
            date,
            settings={'PREFER_DATES_FROM': 'future',
                      'DATE_ORDER': 'DMY'}
        ).strftime("%d-%m-%Y")

    except ValueError:
        return None


def __parse_time(hour):
    """Method to parse the hour to an common format"""

    try:
        hour = hour + ':00' if ':' not in hour else hour
        return dateparser.parse(
            hour,
            settings={'PREFER_DATES_FROM': 'future'}
        ).strftime("%H:%M")

    except ValueError:
        return None


def __usage(handler):
    """Prints usage information with the handler command."""
    return (
        'Usage: *%s* [ %s ] _[ date ] [ hour ] [ name ] [ description ]_'
        % (handler, ' | '.join(VALID_ACTIONS))
    )


def __parse_message(message):
    """Parses the user message to retrieve the action to execute"""

    words = message.text.split()

    if not words:
        return None

    handler = words[0]

    if len(words) < 2:
        return __usage(handler)

    action = words[1]

    if action not in VALID_ACTIONS:
        return __usage(handler)

    date = __parse_date(words[2]) if len(words) > 2 else __parse_date('today')
    hour = __parse_time(words[3]) if len(words) > 3 else None
    name = words[4] if len(words) > 4 else None
    description = ' '.join(words[5:]) if len(words) > 5 else None

    username = message.user.name
    fireteam = Activity(date, hour, name, description)

    return FireteamsCmd(handler, action,
                        message.chat.chat_id,
                        message.user.user_id,
                        fireteam, username)

#
# Misc
#


def __escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

#
# Invocation handlers
#


def __fireteams_handler(message):
    """Method to handle fireteams"""

    cmd = __parse_message(message)

    if not isinstance(cmd, FireteamsCmd):
        return Action(
            name='new_message',
            target=message.chat.chat_id,
            text=cmd,
            markup='markdown'
        )

    else:
        return Action(
            name='new_message',
            target=message.chat.chat_id,
            text=__fireteams_do(cmd),
            markup='markdown'
        )


def kdd(message):
    "This allows to respond to /kdd command."
    return __fireteams_handler(message)


def raid(message):
    "This allows to respond to /kdd command."
    return __fireteams_handler(message)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:

        from pybot.common.message import Message
        from pybot.common.user import User
        from pybot.common.chat import Chat
        user = User(1, 'foo', 'bar', 'rael')
        chat = Chat(1, 'Console', 'Console')
        message = Message(1, user, time.strftime,
                          ' '.join(sys.argv[1:]), chat, None)
        print(kdd(message))

    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
