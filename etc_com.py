import datetime
import os
import random
import re
import sqlite3

from telebot import types

from functions import create_keyboard, get_department
from misc import DB_DIR, supers, CHATS_ID

# -----------------------Разные команды----------------------------------------

def etc_com(bot, message):

    dep = get_department("staff", message.from_user.id)
    gg_path = "/home/irc/bot/pics/"
    kbrd = create_keyboard(dep)

# -----------------------------------------------------------------------------
# ---------------------------ВСЯКИЕ РУЧНЫЕ ТЕСТЫ РАБОТЫ БОТА-------------------
# -----------------------------------------------------------------------------

    # МЕМАСИКИ (ASCII ART)

    if message.text.lower().startswith('мем'):
        memes = types.InlineKeyboardMarkup()
        police_btn = types.InlineKeyboardButton(text='Полиция!', callback_data='police')
        bogdan_btn = types.InlineKeyboardButton(text='Дядя Богдан!', callback_data='bogdan')
        hydra_btn = types.InlineKeyboardButton(text='Гидрааа!', callback_data='hydra')
        hydra_spy_btn = types.InlineKeyboardButton(text='Гидра шпионе!', callback_data='hydrash')
        dilda_btn = types.InlineKeyboardButton(text='Дылда!', callback_data='dilda')
        pirate_btn = types.InlineKeyboardButton(text='Пират!', callback_data='pirate')
        spies_btn = types.InlineKeyboardButton(text='Розвидка!', callback_data='spies')
        kitty_btn = types.InlineKeyboardButton(text='Котя!', callback_data='kitty')
        cock_btn = types.InlineKeyboardButton(text='Петуч!', callback_data='cock')
        byb_btn = types.InlineKeyboardButton(text='ъуъ', callback_data='byb')
        bob_btn = types.InlineKeyboardButton(text='ъоъ', callback_data='bob')
        memes.add(police_btn, bogdan_btn, kitty_btn)
        memes.add(hydra_btn, hydra_spy_btn, pirate_btn)
        memes.add(dilda_btn, spies_btn, cock_btn)
        memes.add(byb_btn, bob_btn)
        bot.send_message(
                chat_id=message.chat.id,
                text='ВЫБИРАЙ ЖЕ!',
                reply_markup=memes)

    