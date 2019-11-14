# -*- coding: utf-8 -*-

import logging

from settings import token
from database import database

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU, CHOOSING, LOOKING = range(3)

db = database()

def start(update, context):
    menu_keyboard = [
        [InlineKeyboardButton("Каталог", callback_data='0')],
        [InlineKeyboardButton("Отзывы", callback_data='1')],
        [InlineKeyboardButton("Гарантии", callback_data='2')],
        [InlineKeyboardButton("Поддержка", callback_data='3')]
    ]
    
    reply_markup = InlineKeyboardMarkup(menu_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        "Главное меню",
        reply_markup=reply_markup
    )

    return MENU

def start_over(update, context):
    querry = update.callback_query
    menu_keyboard = [
        [InlineKeyboardButton("Каталог", callback_data='0')],
        [InlineKeyboardButton("Отзывы", callback_data='1')],
        [InlineKeyboardButton("Гарантии", callback_data='2')],
        [InlineKeyboardButton("Поддержка", callback_data='3')]
    ]
    
    reply_markup = InlineKeyboardMarkup(menu_keyboard, one_time_keyboard=True)

    context.bot.edit_message_text(
        chat_id=querry.message.chat_id,
        message_id=querry.message.message_id,
        text="Главное меню",
        reply_markup=reply_markup
    )

    return MENU

def catalog(update, context):
    querry = update.callback_query
    if(context.user_data.get('offset') == None):
        context.user_data['offset'] = 0
    reply_text = 'Список:\n'
    point = 1
    items = db.get_catalog(offset=context.user_data['offset'])
    for item in items:
        reply_text += f"{point}. {item['name']} - {item['cost']} p.\n"
        point += 1
    keyboard = list()
    for i in range(1, point, point//2):
        keyboard.append([])
        for j in range(i, min(point, i + point//2)):
            callback_data = str(items[j-1]['id'])
            keyboard[-1].append(InlineKeyboardButton(str(j), callback_data=callback_data))
    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='back')
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.edit_message_text(
        chat_id=querry.message.chat_id,
        message_id=querry.message.message_id,
        text=reply_text,
        reply_markup=reply_markup
    )

    return CHOOSING


def catalog_button(update, context):
    querry = update.callback_query
    id = int(querry.data)
    context.user_data['last_id'] = id
    item = db.get_item_by_id(id)
    reply_text = f"{item['name']}\n{item['description']}\n{item['cost']} p."
    keyboard = [
        [InlineKeyboardButton("Перейти к оплате", callback_data='buy')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.edit_message_text(
        chat_id=querry.message.chat_id,
        message_id=querry.message.message_id,
        text=reply_text,
        reply_markup=reply_markup
    )

    return LOOKING

def looking_buy(update, context):
    querry = update.callback_query
    context.bot.send_message(context.job.context, f"Buy id={context.user_data['last_id']}")
    return catalog(update, context)


def other(update, context):
    return MENU


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
                CallbackQueryHandler(catalog, pattern='^0$'),
                CallbackQueryHandler(other, pattern='^[1-3]$')
            ],
            CHOOSING: [
                CallbackQueryHandler(start_over, pattern='^back$'),
                CallbackQueryHandler(catalog_button, pattern='')
            ],
            LOOKING: [
                CallbackQueryHandler(catalog, pattern='^back$'),
                CallbackQueryHandler(looking_buy, pattern='^buy$')
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

