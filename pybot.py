#!/usr/bin/env python

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

def hear(bot, update):
    """Function to handle text messages"""
    log_message(bot, update)

def log_message(bot, update):
    logger.info(update.update_id)
    logger.info(update.message.message_id)
    logger.info(update.message.from_user.first_name)
    logger.info(update.message.from_user.last_name)
    logger.info(update.message.date)
    logger.info(update.message.text)

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
