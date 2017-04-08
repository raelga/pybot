#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 raids.py       Simple fireteam scheduler.
 Author:        David @davlopgom
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

from __future__ import print_function

import datetime
import os
import sys
import re

FILES_PATH = os.path.dirname(__file__) + "/__raids__"

HOURS = ['10:00', '16:00', '20:00', '22:30']
LEVEL = ['hard']

TODAY = datetime.datetime.today()
NEXT_INI = TODAY + datetime.timedelta(days=(8 - TODAY.weekday()))
NEXT_END = NEXT_INI + datetime.timedelta(days=6)
CURR_END = TODAY + datetime.timedelta(days=(7 - TODAY.weekday()))
CURR_INI = CURR_END - datetime.timedelta(days=6)


def format_date(day):
    "Returns a TODAY formated"

    return day.strftime("%d-%m-%y")


def week_file(day):
    "Returns the data file for the day"

    day_arr = day.split('-')
    day = datetime.datetime(
        int(day_arr[2]), int(day_arr[1]), int(day_arr[0]))
    now_wd = TODAY.weekday()
    req_wd = day.weekday()

    week = ''
    if (now_wd == 1) or (now_wd == 0 and req_wd == 0) \
            or (now_wd >= 2 and req_wd >= now_wd):
        week = 'current'
    else:
        week = 'next'

    if week == 'current':
        file_path = FILES_PATH + '/Destiny_' + \
            format_date(CURR_INI) + '_' + format_date(CURR_END) + '.txt'
    if week == 'next':
        file_path = FILES_PATH + '/Destiny_' + \
            format_date(NEXT_INI) + '_' + format_date(NEXT_END) + '.txt'

    return file_path


def convert_date(day):
    "Returns TODAY based on the day"

    iday = None
    if day.lower() == 'lunes':
        iday = int('0')
    elif day.lower() == 'martes':
        iday = int('1')
    elif day.lower() == 'miercoles' or day.lower() == 'miércoles':
        iday = int('2')
    elif day.lower() == 'jueves':
        iday = int('3')
    elif day.lower() == 'viernes':
        iday = int('4')
    elif day.lower() == 'sabado' or day.lower() == 'sábado':
        iday = int('5')
    elif day.lower() == 'domingo':
        iday = int('6')
    elif day.lower() == 'hoy':
        iday = TODAY.weekday()
    elif day.lower() == 'mañana':
        iday = TODAY.weekday() + 1

    if iday:
        day = TODAY + datetime.timedelta(days=(iday - TODAY.weekday()))
        return format_date(day)
    else:
        return day


def create_file(kind, datafile):
    "Create a new file"

    if kind == 'current':
        first_day = CURR_INI
    elif kind == 'next':
        first_day = NEXT_INI

    with open(datafile, 'w') as datafile:
        for i in range(7):
            day = format_date(first_day + datetime.timedelta(days=i))
            datafile.write(day + '\n')
            for difficulty in LEVEL:
                datafile.write(difficulty + '\n')
                for hour in HOURS:
                    datafile.write(hour + '\n')


def new_week():
    "Create new week file"

    if not os.path.exists(FILES_PATH):
        os.makedirs(FILES_PATH)

    current = FILES_PATH + '/Destiny_' + \
        format_date(CURR_INI) + '_' + format_date(CURR_END) + '.txt'

    if not os.path.isfile(current):
        create_file('current', current)

    new_conv = FILES_PATH + '/Destiny_' + \
        format_date(NEXT_INI) + '_' + format_date(NEXT_END) + '.txt'

    if os.path.isfile(new_conv):
        return 'Ya se han creado convocatorias para la siguiente semana.'
    else:
        create_file('next', new_conv)
        return 'Convocatorias creadas!!'


def view_conv(day, difficulty, hour):
    "View the fireteams"
    day_point = None
    diff_point = None
    hour_point = None
    result = []

    if day:
        day = convert_date(day)
        datafile = week_file(day)

        with open(datafile, 'r') as datafile:
            get_all = datafile.readlines()

        for i, line in enumerate(get_all):
            if day.lower() in line.lower():
                day_point = i
            elif day_point and difficulty.lower() in line.lower():
                diff_point = i
                day_point = None
            elif diff_point and hour.lower() in line.lower():
                hour_point = i
                diff_point = None
            elif hour_point:
                hour = re.search(r'^(\d).', line, re.I)
                if hour:
                    hour_point = i
                else:
                    hour_point = None
            elif re.search(r'^\d\d-\d\d-\d\d', line, re.I):
                day_point = None
                diff_point = None
                hour_point = None

            if day_point:
                result.append(line)
            elif diff_point:
                result.append(line)
            elif hour_point:
                result.append(line)

        if result:
            return ''.join(result)
        else:
            return 'No se ha encontrado esa convocatoria.'

    else:
        current_file = FILES_PATH + '/Destiny_' + \
            format_date(CURR_INI) + '_' + format_date(CURR_END) + '.txt'
        return current_file


def manage_player(name, day, difficulty, hour):
    "Manage player"
    day_point = None
    diff_point = None
    hour_point = None
    delete_point = None
    newline = None
    dropline = None
    pos = int(1)
    day = convert_date(day)
    filepath = week_file(day)
    result = 'No se ha encontrado esa convocatoria.'

    with open(filepath, 'r') as ro_file:
        get_all = ro_file.readlines()

    with open(filepath, 'w') as rw_file:
        for i, line in enumerate(get_all):
            if day.lower() in line.lower():
                day_point = i
            elif day_point and difficulty.lower() in line.lower():
                diff_point = i
                day_point = None
            elif diff_point and hour.lower() in line.lower():
                hour_point = i
                diff_point = None
            elif hour_point:
                already_listed = re.search(
                    r'^(\d).\s' + name + '\n', line, re.I)
                user_listed = re.search(r'^(\d)\.\s', line, re.I)
                if already_listed:
                    delete_point = i
                    result = 'Jugador eliminado.'
                elif user_listed and delete_point:
                    pos = int(user_listed.group(1)) - 1
                    dropline = line.replace(user_listed.group(1), str(pos))
                elif delete_point:
                    delete_point = None
                    hour_point = None
                elif user_listed:
                    pos = int(user_listed.group(1)) + 1
                else:
                    newline = str(pos) + '. ' + name + '\n'
                    result = 'Jugador añadido.'
                    hour_point = None

            if dropline:
                rw_file.writelines(dropline)
                dropline = None
            elif newline:
                rw_file.writelines(newline)
                rw_file.writelines(line)
                newline = None
            elif delete_point is None:
                rw_file.writelines(line)

    return result


def dispatcher(words):
    "Command parser and dispatcher"

    newweek = re.search(r'(?:^.|^)\braid\b.*crea.*conv.*',
                        words, re.I | re.M)
    viewconv = re.search(
        r'(?:^.|^)\braid\b.*ver.*conv\S*\s*(\S*)\s*(\S*)\s*(\S*)',
        words, re.I | re.M)
    manage = re.search(
        r'(?:^.|^)\braid\b\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)',
        words, re.I | re.M)

    if newweek:

        return new_week()

    elif viewconv:

        conv_date = viewconv.group(1)
        conv_level = viewconv.group(2)
        conv_hour = viewconv.group(3)

        if ':' not in conv_hour and ':' in conv_level:
            conv_level = '***'
            conv_hour = '***'
        else:
            conv_hour = '***'

        return view_conv(conv_date, conv_level, conv_hour)

    elif manage:

        name = manage.group(1)
        conv_date = manage.group(2)
        conv_level = manage.group(3)
        conv_hour = manage.group(4)
        return manage_player(name, conv_date, conv_level, conv_hour)


def hear(words):
    "Implements hear to recieve the messages"
    return dispatcher(words)


def main(argv):
    "This method allows to execute the plugin in standalone mode"

    if len(argv) > 1:
        print(hear(argv[1]))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
