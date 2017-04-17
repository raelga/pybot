#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 pyboy.py       Telegram adapter for pybot using python-telegram-bot.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Export TELEGRAM_TOKEN variable and run the bot.
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import os
import logging
from importlib import reload
from subprocess import check_output

import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    CallbackQueryHandler, Filters
import pybot.brain as brain

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

LOG = logging.getLogger(__name__)


def update_yourself(bot, update):
    "Pulls the git repo to update its own code."
    output = check_output(["git", "pull"]).decode("utf-8")
    reload(brain)

    LOG.info(output)
    bot.sendMessage(update.message.chat_id, text=output)


def error(bot, update, error_message):
    "Error handler function"
    LOG.warning('Update "%s" caused error "%s" for %s',
                update, error_message, bot.id)


def interact(bot, update, action):
    "Handler for interactions"
    responses = brain.interact(action, update)

    if responses:
        speak(bot, update, responses)


def hear(bot, update):
    "Handler for text messages"

    cmd = re.search(r'^(!|\/)(\w+)\s?.*', update.message.text)

    if cmd:

        interact(bot, update, cmd.groups()[1])

    else:

        thoughts = brain.ears(update.message.text)

        remember(bot, update)
        if thoughts:
            speak(bot, update, thoughts)


def speak(bot, update, thoughts):
    "Handler for bot text responses."

    LOG.info('I\'ve got something to say.')
    for words in thoughts:
        if os.path.isfile(words):
            show(bot, update, words, 'file')
        elif words.startswith('http'):
            show(bot, update, words, 'url')
        else:
            bot.sendMessage(update.message.chat_id, text=words)


def show(bot, update, stuff, media_type):
    "Handler for bot responses when he need more than words."

    LOG.info('I\'ve got something to show.')

    try:

        if media_type == 'file':
            thing = open(stuff, 'rb')
        elif media_type == 'url':
            if requests.get(stuff).status_code == 200:
                thing = stuff
            else:
                LOG.warning("%s is not available.", stuff)
        else:
            thing = stuff

        if thing and stuff.lower().endswith(('.png', '.jpg', '.jpeg')):
            bot.sendispatcher.oto(update.message.chat_id, photo=thing)
        elif thing:
            bot.sendDocument(update.message.chat_id, document=thing)

    except OSError as err:
        LOG.warning("I can't show the %s. (%s)", stuff, err)
        bot.sendMessage(update.message.chat_id, text=stuff)


def view(bot, update):
    "Function to handle photo messages."

    thoughts = brain.eyes(bot.getFile(
        update.message.photo[-1].file_id).file_path)
    print(thoughts)
    remember(bot, update)
    if thoughts:
        speak(bot, update, thoughts)


def events(bot, update):
    "Function to handle group events."

    if update.message.new_chat_member is not None:
        LOG.info('New member')
        interact(bot, update, 'user_entering')

    if update.message.left_chat_member is not None:
        LOG.info('Member left')
        interact(bot, update, 'user_leaving')

    remember(bot, update)


def menu_from_array(data, exit_button=None, columns=2):
    "Function to convert an array to Telegram InlineKeyboard."

    menu = []
    menu.append([])

    i = 0
    for column in enumerate(data):

        if re.search(r'^http:|https:.*', data[column][1]):
            menu[i].append(
                telegram.InlineKeyboardButton(data[column][0],
                                              url=data[column][1]))
        else:
            menu[i].append(
                telegram.InlineKeyboardButton(data[column][0],
                                              callback_data=data[column][1]))

        if not (column + 1) % columns:
            menu.append([])
            i += 1

    if exit_button:
        menu.append([telegram.InlineKeyboardButton(
            exit_button[0], callback_data=exit_button[1])])

    return telegram.InlineKeyboardMarkup(menu)


def show_menu(bot, update):
    "Function to print a dynamic menu"

    data = brain.menu(update.message.from_user.id)
    menu = menu_from_array(data, columns=3)

    return bot.sendMessage(update.message.chat_id,
                           text='Pulsa para desplegar',
                           parse_mode=telegram.ParseMode.HTML,
                           reply_markup=menu)


def update_message(bot, message, text, menu=None):
    "Update an existing message"

    if menu:

        bot.editMessageText(text=text,
                            parse_mode=telegram.ParseMode.HTML,
                            reply_markup=menu,
                            chat_id=message.chat_id,
                            message_id=message.message_id)

    else:

        bot.editMessageText(text=text,
                            chat_id=message.chat_id,
                            message_id=message.message_id)


def callback_handler(bot, update):
    """Function to handle the telegram callbacks"""

    query = update.callback_query

    if query.data == 'exit':

        update_message(bot, query.message, '🙊')

    elif query.data == 'home':

        data = brain.menu(query.from_user.id)
        menu = menu_from_array(data, ['x close', 'exit'])

        update_message(bot, query.message, query.data, menu)

    elif re.search(r'^_.*', query.data):

        data = brain.submenu(query.data, query.from_user.id)
        menu = menu_from_array(data, ['< back', 'home'])

        update_message(bot, query.message, query.data, menu)

    else:

        thoughts = brain.ears(query.data)
        if thoughts:
            speak(bot, query, thoughts)


def remember(bot, update):
    """Handler to store all message info in the brain."""

    brain.remember(whoami=bot.id,
                   when=update.message.date,
                   where=update.message.chat_id,
                   who=update.message.from_user.id,
                   what=update.message.text)


def start():
    """Retrieves messages from the telegram API."""

    updater = Updater(os.environ['TELEGRAM_TOKEN'])
    dispatcher = updater.dispatcher

    LOG.info('Bot %s up and ready!', (dispatcher.bot.username))

    # Specific handlers
    dispatcher.add_handler(MessageHandler(Filters.photo, view))
    dispatcher.add_handler(MessageHandler(Filters.status_update, events))
    dispatcher.add_handler(CommandHandler("update_yourself", update_yourself))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Default handler
    dispatcher.add_handler(MessageHandler(Filters.all, hear))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    start()
