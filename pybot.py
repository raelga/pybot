#!/usr/bin/env python
"""
 pyboy.py       Telegram bot using python-telegram-bot.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Export TELEGRAM_TOKEN variable and run the bot. 
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import os

from telegram import InlineQueryResultArticle, ForceReply, \
        ParseMode, InputTextMessageContent, Emoji, \
        InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, \
    MessageHandler, CallbackQueryHandler, Filters

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

def error(bot, update, error):
    """Error handler function"""
    logger.warn('Update "%s" caused error "%s"' % (update, error))

import brain

def hear(bot, update):
    """Function to handle text messages"""
    thoughts = brain.ears(update.message.text)

    remember(bot, update)
    speak(bot, update, thoughts)

from urllib.parse import urlparse

def speak(bot, update, thoughts):
    """Function to handle bot responses"""
    for words in thoughts:
        if os.path.isfile(words):
            show(bot, update, words, 'file')
        elif urlparse(words):
            show(bot, update, words, 'url')
        else:
            bot.sendMessage(update.message.chat_id, text=words)

def show(bot, update, stuff, type):
    """Function to handle bot responses when he need more than words"""
    try:
        if type == 'file':
            try:
                thing = open(stuff, 'rb')
            except:
                logger.warn("I can't open the %s" % stuff)
        else:
            thing = stuff

        if stuff.lower().endswith(('.png', '.jpg', '.jpeg')):
            bot.sendPhoto(update.message.chat_id, photo=thing)

    except:
        logger.warn("I can't show the %s" % stuff)         
        bot.sendMessage(update.message.chat_id, text=stuff)

def remember(bot, update):
    m = update.message
    brain.remember(m.date, m.chat_id, m.from_user.id, m.text)

def main():
    updater = Updater(os.environ['TELEGRAM_TOKEN'])
    dp = updater.dispatcher
    logger.info('Bot %s up and ready!' % (dp.bot.username))

    # Message handlers
    dp.add_handler(MessageHandler([Filters.text], hear))

    # Command definitions
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
