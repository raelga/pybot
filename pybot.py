#!/usr/bin/env python
"""
 pyboy.py       Telegram bot using python-telegram-bot.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Export TELEGRAM_TOKEN variable and run the bot.
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import random
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

from subprocess import check_output
from importlib import reload

def update_yourself(bot, update):

    output = check_output(["git", "pull"]).decode("utf-8")
    reload(brain)

    logger.info(output)
    bot.sendMessage(update.message.chat_id, text=output)

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
    if thoughts: speak(bot, update, thoughts)

    m = update.message

    if ( m.chat_id == -1001056495683 ) and ( m.from_user.id == 51267720 ):
        bot.sendDocument(m.chat_id, document="http://thecatapi.com/api/images/get?format=src&type=gif&timestamp=" + str(random.random()) + ".gif")

import requests

def speak(bot, update, thoughts):
    """Function to handle bot responses"""
    logger.info('I\'ve got something to say.')
    for words in thoughts:
        if os.path.isfile(words):
            show(bot, update, words, 'file')
        elif words.startswith('http'):
            show(bot, update, words, 'url')
        else:
            bot.sendMessage(update.message.chat_id, text=words)

def groups_hardcoded(bot, update):

    rmk = InlineKeyboardMarkup([
                    [InlineKeyboardButton('Destiny', url='https://telegram.me/pkts_destiny')],
                    [InlineKeyboardButton('Overwatch', url='https://telegram.me/pkts_overwatch')],
                    [InlineKeyboardButton('Battlefield', url='https://telegram.me/pkts_battlefield')],
                    [InlineKeyboardButton('Final Fantasy', url='https://telegram.me/joinchat/AzNL9D_0xS_0h6Q3H5m69Q')],
                    [InlineKeyboardButton('Grand Theft Auto', url='https://telegram.me/joinchat/AzNL9ECAaKh4y3za3egFbw')],
                    [InlineKeyboardButton('Space Exploration', url='https://telegram.me/joinchat/AzNL9EAy0gzR3etQ_Q4JSw')],
                    [InlineKeyboardButton('Division', url='https://telegram.me/joinchat/ANSWpD4TPEtu5wGU6O7J3Q')],
                    [InlineKeyboardButton('Souls', url='https://telegram.me/joinchat/AzNL9ACpL0yP02kER67Mhg')],
                    [InlineKeyboardButton('Borlderlands', url='https://telegram.me/joinchat/AzNL9AD3n5pKH_6e1trOZA')],
                    [InlineKeyboardButton('Hearthstone', url='https://telegram.me/joinchat/AzNL9D7UHCsWDtfgz1cw3g')],
                    [InlineKeyboardButton('PC Master Race', url='https://telegram.me/joinchat/AzNL9EFBO0e81gXlECiRzA')],
                    [InlineKeyboardButton('Pokémon', url='https://telegram.me/joinchat/AzNL9D-KxgBdpa9RlWF2kg')],
                    [InlineKeyboardButton('Miscelánea', url='https://telegram.me/miscelanea')],
                   ])

    bot.sendMessage(update.message.chat_id, text="Listado de grupos, pulsa para unirte.", reply_markup=rmk)


def show(bot, update, stuff, type):
    """Function to handle bot responses when he need more than words"""
    logger.info('I\'ve got something to show.')
    try:
        if type == 'file':
            try:
                thing = open(stuff, 'rb')
            except:
                logger.warn("I can't open the %s" % stuff)
        elif type == 'url':
            try:
                if requests.get(stuff).status_code == 200:
                    thing = stuff
                else:
                    logger.warn("%s is not available." % stuff)
            except:
                logger.warn("%s is not a URL." % stuff)
        else:
            thing = stuff

        if thing and stuff.lower().endswith(('.png', '.jpg', '.jpeg')):
            bot.sendPhoto(update.message.chat_id, photo=thing)

    except:
        logger.warn("I can't show the %s" % stuff)
        bot.sendMessage(update.message.chat_id, text=stuff)

def view(bot, update):
    """Function to handle photo messages"""
    logger.info('I see stuff.')
    thoughts = brain.eyes(update.message.text)

    remember(bot, update)
    if thoughts: speak(bot, update, thoughts)

    m = update.message
    if ( m.chat_id == -1001056495683 ) and ( m.from_user.id == 51267720 ):
        bot.sendDocument(m.chat_id, document="http://thecatapi.com/api/images/get?format=src&type=gif&timestamp=" + str(random.random()) + ".gif")

def remember(bot, update):
    m = update.message
    brain.remember(m.date, m.chat_id, m.from_user.id, m.text)

def main():
    updater = Updater(os.environ['TELEGRAM_TOKEN'])
    dp = updater.dispatcher
    logger.info('Bot %s up and ready!' % (dp.bot.username))

    # Message handlers
    dp.add_handler(MessageHandler([Filters.text], hear))
    dp.add_handler(MessageHandler([Filters.photo], view))

    # Command definitions
    dp.add_handler(CommandHandler("battletags", hear))
    dp.add_handler(CommandHandler("groups", groups_hardcoded))
    dp.add_handler(CommandHandler("update_yourself", update_yourself))

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
