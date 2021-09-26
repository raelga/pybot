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
from typing import Text

import requests
import telegram
from telegram import Update
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram.ext.callbackcontext import CallbackContext
import pybot.brain as brain
from pybot.common.action import Action
from pybot.common.chat import Chat
from pybot.common.message import Message
from pybot.common.user import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

LOG = logging.getLogger(__name__)


def kill_process(pid: int):

    pgrp = os.getpgid(pid)
    os.killpg(pgrp, signal.SIGINT)
    out = check_output(["ps", "auxf"])
    print(out.decode('utf-8'))


def update_yourself(update: Update, ctx: CallbackContext):
    "Pulls the git repo to update its own code."

    repo_url = "git://github.com/raelga/pybot"
    repo_branch = "main"

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
        speak(ctx.bot, update, response)
    else:
        if err:
            LOG.error(err.decode('utf-8'))
        speak(ctx.bot, update, "Ignoring update, something went wrong.")


def error(update: Update, ctx: CallbackContext):
    "Error handler function"
    LOG.error('Update "%s" caused error "%s" for %s',
              update, ctx.error.args, ctx.bot.id)


def message_from_update(ctx: CallbackContext, update: Update, media=None):
    "Define a pybot message based on the telegram meesage"

    try:
        uchat = ctx.bot.getChat(chat_id=update.message.from_user.id)
    except telegram.TelegramError as err:
        LOG.warning("Error: (%s)", err)

    pybot_user = User(
        user_id=update.message.from_user.id,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
        bio=uchat.bio,
        username=update.message.from_user.username,
        human=(not(update.message.from_user.is_bot))
    )

    pybot_chat = Chat(
        chat_id=update.message.chat.id,
        chat_type=update.message.chat.type,
        chat_name=update.message.chat.title
    )

    pybot_message = Message(
        message_id=update.message.message_id,
        user=pybot_user,
        chat=pybot_chat,
        date=update.message.date,
        text=update.message.text,
        media=media
    )

    return pybot_message


def interact(ctx: CallbackContext, update: Update,  action):
    "Handler for interactions"

    responses = brain.interact(action, message_from_update(ctx, update))

    if responses:
        communicate(ctx, update, responses)


def hear(update: Update, ctx: CallbackContext):
    "Handler for text messages"

    try:
        cmd = re.search(r'^(!|\/)(\w+)\s?.*', update.message.text)
    except telegram.TelegramError as err:
        LOG.warning("Error: (%s)", err)

    if cmd:

        interact(ctx, update, cmd.groups()[1].lower())

    else:

        interact(ctx, update, 'interact')

    thoughts = brain.ears(update.message.text)

    remember(ctx, update)

    if thoughts:
        communicate(ctx, update, thoughts)


def view(update: Update, ctx: CallbackContext):
    "Function to handle photo messages."

    url = ctx.bot.getFile(
        update.message.photo[-1].file_id).file_path

    thoughts = brain.eyes(url)

    remember(ctx, update, media=url)

    if thoughts:
        communicate(ctx, update, thoughts)


def listen(update: Update, ctx: CallbackContext):
    "Function to handle photo messages."

    url = ctx.bot.getFile(update.message.voice.file_id).file_path

    thoughts = brain.interact('listen', message_from_update(ctx, update, url))

    remember(ctx, update, media=url)

    if thoughts:
        communicate(ctx, update, thoughts)


def events(update: Update, ctx: CallbackContext):
    "Function to handle group events."

    if update.message.new_chat_member is not None:
        LOG.info('New member')
        interact(ctx, update, 'user_entering')

    if update.message.left_chat_member is not None:
        LOG.info('Member left')
        interact(ctx, update, 'user_leaving')

    remember(ctx, update)


def communicate(ctx: CallbackContext, update: Update, thoughts):
    "Handler for bot text responses."

    for thought in thoughts:

        if isinstance(thought, str):

            if os.path.isfile(thought):
                show(ctx, update, thought, 'file')
            elif thought.startswith('http'):
                show(ctx, update, thought, 'url')
            else:
                speak(ctx, update, thought)

        elif isinstance(thought, Action):

            execute(ctx, update, thought)


def speak(ctx: CallbackContext, update: Update, words: str, language=None):
    "Handler for bot text responses."

    LOG.info('I\'ve got something to say in %s: "%s"' %
             (update.message.chat_id, words))

    if language:

        ctx.bot.sendMessage(update.message.chat_id,
                            text=words, parse_mode=language)
    else:

        ctx.bot.sendMessage(update.message.chat_id, text=words)


def show(ctx: CallbackContext,  update: Update, stuff, media_type, reply_markup=None):
    "Handler for bot responses when he need more than words."

    LOG.info('I\'ve got something to show in %s: "%s"' %
             (update.message.chat_id, stuff))

    if reply_markup:

        ctx.bot.sendMessage(update.message.chat_id,
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

                ctx.bot.sendPhoto(update.message.chat_id, photo=thing)

            elif thing:

                ctx.bot.sendDocument(update.message.chat_id, document=thing)

        except OSError as err:
            LOG.warning("I can't show the %s. (%s)", stuff, err)
            ctx.bot.sendMessage(update.message.chat_id, text=stuff)


def edit(ctx: CallbackContext, update: Update, text: str, reply_markup=None):
    "Update an existing message"

    if reply_markup:

        ctx.bot.editMessageText(text=text,
                                parse_mode=telegram.ParseMode.HTML,
                                reply_markup=reply_markup,
                                chat_id=update.message.chat_id,
                                message_id=update.message.message_id)

    else:

        ctx.bot.editMessageText(text=text,
                                chat_id=update.message.chat_id,
                                message_id=update.message.message_id)


def callback_handler(update: Update, ctx: CallbackContext):
    """Function to handle the telegram callbacks"""
    interact(ctx, update.callback_query, update.callback_query.data)


def execute(ctx: CallbackContext, update: Update,  action):
    "Function to print a dynamic menu"

    if action.name == 'edit_message':

        if action.markup == 'menu':

            edit(ctx, update, action.text,
                 reply_markup=get_menu(action.payload))

        elif action.text:

            edit(ctx, update, action.text)

    elif action.name == 'new_message':

        if action.markup == 'menu':

            show(ctx, update, action.text,
                 media_type=telegram.ParseMode.HTML,
                 reply_markup=get_menu(action.payload))

        elif action.markup == 'markdown':

            speak(ctx, update, action.text,
                  language=telegram.ParseMode.MARKDOWN)

        elif action.markup == 'html':

            speak(ctx, update, action.text,
                  language=telegram.ParseMode.HTML)

        elif action.text:

            speak(ctx, update, action.text)

    elif action.name == 'list_admins':

        admins = get_admins(ctx, update)
        if admins != None:
            for admin in admins:
                action.text += " " + admin.user.name
            speak(ctx, update, action.text,
                  language=telegram.ParseMode.HTML)


def get_admins(ctx: CallbackContext, update: Update):
    try:
        return ctx.bot.getChatAdministrators(
            chat_id=update.message.chat_id, timeout=8
        )
    except TimeoutExpired as exception:
        LOG.warning("Timeout while fetching chat admins. (%s)", exception)
    except TypeError as err:
        LOG.warning("Unable to fetch chat admins: (%s)", err)
    except telegram.error.BadRequest as err:
        LOG.warning(err.message)
    return None


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


def remember(ctx: CallbackContext, update: Update, media=None):
    """Handler to store all message info in the brain."""

    brain.remember(message_from_update(ctx, update, media))


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
