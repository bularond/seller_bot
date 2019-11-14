# -*- coding: utf-8 -*-

import logging

from settings import token
from database import database

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU, CHOOSING, LOOKING = range(3)

db = database()

def start(update, context):
    menu_keyboard = [
        ["Каталог"],
        ["Отзывы"],
        ["Гарантии"],
        ["Поддержка"]
    ]
    markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)

    update.message.reply_text("Entire message",
            reply_markup=markup)

    return MENU


def catalog(update, context):
    text = update.message.text
    if(context.user_data.get('offset') == None):
        context.user_data['offset'] = 0
    reply_text = 'List:\n'
    point = 1
    ls = db.get_catalog(offset=context.user_data['offset'])
    for item in ls:
        reply_text += f"{point}. {item['name']} - {item['cost']} p.\n"
        point += 1
    keyboard = list()
    for i in range(1, point, 5):
        keyboard.append([])
        for j in range(i, min(point, i + 5)):
            keyboard[-1].append(str(j))
    keyboard.append([
        'Back'
    ])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(reply_text, reply_markup=reply_markup)

    return CHOOSING


def catalog_button(update, context):
    text = update.message.text
    if(text == 'Back'):
        return start(update, context)
    else:
        id = context.user_data['offset'] + int(text) - 1
        context.user_data['last_id'] = id
        item = db.get_item_by_id(id)
        reply_text = f"{item['name']}\n{item['description']}\n{item['cost']} p."
        keyboard = [
            [KeyboardButton('Buy'), KeyboardButton('Back')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(reply_text, reply_markup=reply_markup)

        return LOOKING


def looking_button(update, context):
    text = update.message.text
    if(text == 'Back'):
        return catalog(update, context)
    elif(text == 'Buy'):
        #TODO
        update.message.reply_text(f"Buy id={context.user_data['last_id']}")
        return catalog(update, context)


def other(update, context):
    pass


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
            ],
            CHOOSING: [
                MessageHandler(Filters.regex('^(0|1|2|3|4|5|6|7|8|9|10|Back)$'),
                               catalog_button)
            ],
            LOOKING: [
                MessageHandler(Filters.regex('^(Buy|Back)$'),
                               looking_button)
            ]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

