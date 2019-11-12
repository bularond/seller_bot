# -*- coding: utf-8 -*-

import logging

from settings import token

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU, CHOOSING = range(2)

keyboard = [["Catalog"],
            ["Reviews"],
            ["Guarantee"],
            ["Support"]
        ]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def start(update, context):
    update.message.reply_text("Entire message",
            reply_markup=markup)
    return MENU


def catalog(update, context):
    text = update.message.text
    update.message.reply_text(
        "*Catalog:*"
    )
    return CHOOSING

def other(update, context):
    text = update.message.text
    
    rerurn MENU

def done(update, context):
    update.message.reply_text("Something went wrong")
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('^Catalog$'),
                               catalog),
                MessageHandler(Filters.regex('^(Reviews|Guarantee|Support)$'),
                               other)
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

