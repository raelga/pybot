#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 pyboy.py       Telegram adapter for pybot using python-telegram-bot.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Export TELEGRAM_TOKEN variable and run the bot.
 Tested on:     Python 3 / OS X 10.11.5
"""
import logging
import os
import re
from importlib import reload
from subprocess import Popen, PIPE, TimeoutExpired

import requests
import telegram
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

import pybot.brain as brain
from pybot.common.action import Action
from pybot.common.chat import Chat
from pybot.common.message import Message
from pybot.common.user import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

LOG = logging.getLogger(__name__)


def kill_process(pid):

    pgrp = os.getpgid(pid)
    os.killpg(pgrp, signal.SIGINT)
    out = check_output(["ps", "auxf"])
    print(out.decode('utf-8'))


def update_yourself(bot, update):
    "Pulls the git repo to update its own code."

    repo_url = "git://github.com/raelga/pybot"
    repo_branch = "master"

    if os.environ['GITHUB_REPO']:
        repo_url = os.environ['GITHUB_REPO']

    if os.environ['GITHUB_BRANCH']:
        repo_branch = os.environ['GITHUB_BRANCH']

    try:

        update_cmd = ['git', 'pull', repo_url, repo_branch]
        proc = Popen(update_cmd, stdout=PIPE,
                     stderr=PIPE, preexec_fn=os.setsid)

        out, err = proc.communicate(timeout=5)

    except TimeoutExpired as exception:
        LOG.error(exception)
        proc.kill()
        response = "Ignoring updatem, execution timed out."
    except OSError as exception:
        LOG.error(exception)
    else:
        response = out.decode('utf-8')
        reload(brain)

    if response:
        speak(bot, update, response)
    else:
        if err:
            LOG.error(err.decode('utf-8'))
        speak(bot, update, "Ignoring update, something went wrong.")


def error(bot, update, error_message):
    "Error handler function"
    LOG.error('Update "%s" caused error "%s" for %s',
              update, error_message, bot.id)


def message_from_update(update, media=None):
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
        text=update.message.text,
        media=media)

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

        interact(bot, update, cmd.groups()[1].lower())

    else:

        interact(bot, update, 'interact')

    thoughts = brain.ears(update.message.text)

    remember(bot, update)
    if thoughts:
        communicate(bot, update, thoughts)


def view(bot, update):
    "Function to handle photo messages."

    url = bot.getFile(
        update.message.photo[-1].file_id).file_path

    thoughts = brain.eyes(url)

    remember(bot, update, media=url)
    if thoughts:
        communicate(bot, update, thoughts)


def listen(bot, update):
    "Function to handle photo messages."
    url = bot.getFile(update.message.voice.file_id).file_path

    thoughts = brain.interact('listen', message_from_update(update, url))

    remember(bot, update, media=url)

    if thoughts:
        communicate(bot, update, thoughts)


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


def speak(bot, update, words, language=None):
    "Handler for bot text responses."

    LOG.info('I\'ve got something to say in %s: "%s"' %
             (update.message.chat_id, words))

    if language:

        bot.sendMessage(update.message.chat_id,
                        text=words, parse_mode=language)
    else:

        bot.sendMessage(update.message.chat_id, text=words)


def show(bot, update, stuff, media_type, reply_markup=None):
    "Handler for bot responses when he need more than words."

    LOG.info('I\'ve got something to show in %s: "%s"' %
             (update.message.chat_id, stuff))

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

        if action.markup == 'menu':

            edit(bot, update, action.text,
                 reply_markup=get_menu(action.payload))

        elif action.text:

            edit(bot, update, action.text)

    elif action.name == 'new_message':

        if action.markup == 'menu':

            show(bot, update, action.text,
                 media_type=telegram.ParseMode.HTML,
                 reply_markup=get_menu(action.payload))

        elif action.markup == 'markdown':

            speak(bot, update, action.text,
                  language=telegram.ParseMode.MARKDOWN)

        elif action.markup == 'html':

            speak(bot, update, action.text,
                  language=telegram.ParseMode.HTML)

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


def remember(bot, update, media=None):
    """Handler to store all message info in the brain."""

    brain.remember(message_from_update(update, media=media))


def start():
    """Retrieves messages from the telegram API."""

    updater = Updater(os.environ['TELEGRAM_TOKEN'])
    dispatcher = updater.dispatcher

    LOG.info('Bot %s up and ready!', (dispatcher.bot.username))

    # Specific handlers
    dispatcher.add_handler(MessageHandler(Filters.photo, view))
    dispatcher.add_handler(MessageHandler(Filters.voice, listen))
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
