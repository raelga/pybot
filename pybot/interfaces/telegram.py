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

from pybot.common.user import User
from pybot.common.chat import Chat
from pybot.common.message import Message
from pybot.common.action import Action

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


def message_from_update(update):
    "Define a pybot message based on the telegram meesage"

    pybot_user = User(
        user_id=update.message.from_user.id,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
        username=update.message.from_user.username,
        specie=update.message.from_user.type)

    pybot_chat = Chat(
        chat_id=update.message.chat.id,
        chat_type=update.message.chat.type,
        chat_name=update.message.chat.title)

    pybot_message = Message(
        message_id=update.message.message_id,
        user=pybot_user,
        chat=pybot_chat,
        date=update.message.date,
        text=update.message.text)

    return pybot_message


def interact(bot, update, action):
    "Handler for interactions"

    responses = brain.interact(action, message_from_update(update))

    if responses:
        communicate(bot, update, responses)


def hear(bot, update):
    "Handler for text messages"

    cmd = re.search(r'^(!|\/)(\w+)\s?.*', update.message.text)

    if cmd:

        interact(bot, update, cmd.groups()[1])

    else:

        interact(bot, update, 'interact')

    thoughts = brain.ears(update.message.text)

    remember(bot, update)
    if thoughts:
        communicate(bot, update, thoughts)


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


def communicate(bot, update, thoughts):
    "Handler for bot text responses."

    for thought in thoughts:

        if isinstance(thought, str):

            if os.path.isfile(thought):
                show(bot, update, thought, 'file')
            elif thought.startswith('http'):
                show(bot, update, thought, 'url')
            else:
                speak(bot, update, thought)

        elif isinstance(thought, Action):

            execute(bot, update, thought)


def speak(bot, update, words):
    "Handler for bot text responses."

    LOG.info('I\'ve got something to say.')

    bot.sendMessage(update.message.chat_id, text=words)


def show(bot, update, stuff, media_type, reply_markup=None):
    "Handler for bot responses when he need more than words."

    LOG.info('I\'ve got something to show.')

    if reply_markup:

        bot.sendMessage(update.message.chat_id,
                        text=stuff,
                        parse_mode=media_type,
                        reply_markup=reply_markup)
    else:

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

                bot.sendPhoto(update.message.chat_id, photo=thing)

            elif thing:

                bot.sendDocument(update.message.chat_id, document=thing)

        except OSError as err:
            LOG.warning("I can't show the %s. (%s)", stuff, err)
            bot.sendMessage(update.message.chat_id, text=stuff)


def edit(bot, update, text, reply_markup=None):
    "Update an existing message"

    if reply_markup:

        bot.editMessageText(text=text,
                            parse_mode=telegram.ParseMode.HTML,
                            reply_markup=reply_markup,
                            chat_id=update.message.chat_id,
                            message_id=update.message.message_id)

    else:

        bot.editMessageText(text=text,
                            chat_id=update.message.chat_id,
                            message_id=update.message.message_id)


def callback_handler(bot, update):
    """Function to handle the telegram callbacks"""
    interact(bot, update.callback_query, update.callback_query.data)


def execute(bot, update, action):
    "Function to print a dynamic menu"

    if action.name == 'edit_message':

        if action.payload:

            edit(bot, update, action.text,
                 reply_markup=get_menu(action.payload))

        elif action.text:

            edit(bot, update, action.text)

    elif action.name == 'new_message':

        if action.payload:

            show(bot, update, action.text,
                 media_type=telegram.ParseMode.HTML,
                 reply_markup=get_menu(action.payload))

        elif action.text:

            speak(bot, update, action.text)


def get_menu(data, columns=2):
    "Function to convert an array to Telegram InlineKeyboard."

    menu = []
    menu.append([])

    i = 0
    for option in enumerate(data):

        if not option[1]:
            # Insert blank elements to emulate a separator
            blank = (option[0] + 1) % columns
            while blank:
                menu.append([])
                blank -= 1

        elif re.search(r'^http:|https:.*', option[1][1]):

            menu[i].append(
                telegram.InlineKeyboardButton(option[1][0],
                                              url=option[1][1]))
        else:
            menu[i].append(
                telegram.InlineKeyboardButton(option[1][0],
                                              callback_data=option[1][1]))

        if not (option[0] + 1) % columns:
            menu.append([])
            i += 1

    return telegram.InlineKeyboardMarkup(menu)


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
