import random

from geese import *
from functions import *
from misc import PICS_DIR, DB_DIR

import fix_break


def other_callbacks(bot, call):
#    if call.data == "bro":
        # Ярика 265492010 Москвина 291100413
#            photos = []
#            with open(PICS_DIR+'gg.txt', 'r') as file:
#                photos = file.readlines()
#            bot.send_photo(
#                    chat_id=291100413,
#                    photo=photos[random.randint(0, len(photos)-1)].strip())
#        except Exception as e:
#            print("IN other_callbacks\n{}".format(e))

    if call.data == 'memes':
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
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='ВЫБИРАЙ ЖЕ!',
                reply_markup=memes)
    elif call.data == 'police':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=POLICE)
    elif call.data == 'bogdan':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=BOGDAN)
    elif call.data == 'hydra':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=HYDRA)
    elif call.data == 'hydrash':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=HYDRA_SPY)
    elif call.data == 'spies':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=SPIES)
    elif call.data == 'dilda':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=DILDA)
    elif call.data == 'pirate':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=PIRATE)
    elif call.data == 'kitty':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=KITTY)
    elif call.data == 'cock':
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=COCK)
    elif call.data == 'byb':
            byb = open(PICS_DIR+'byb.jpg', 'rb')
            bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id)
            bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=byb)
    elif call.data == 'bob':
        bob = open(PICS_DIR+'bob.jpg', 'rb')
        bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)
        bot.send_photo(
                chat_id=call.message.chat.id,
                photo=bob)

    elif call.data == 'cons':
        """Отправка списка консультантов по команде"""
        sql = """SELECT uid, last_name, first_name
                FROM staff
                WHERE department=1 or department=2
                ORDER BY department, last_name"""
        text = 'РАБОТЯГИ\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'supers':
        """Отправка списка супервизоров по команде"""
        sql = """SELECT su.uid, de.value, su.last_name, su.first_name
                FROM supers as su
                LEFT JOIN departments as de ON su.department = de.id
                ORDER BY last_name"""
        text = 'СУПЕРВИЗОРЫ\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'helpers':
        """Отправка списка помогаторов по команде ."""
        sql = """SELECT he.uid, de.value, he.last_name, he.first_name
                FROM helpers as he
                LEFT JOIN departments as de ON he.department = de.id
                ORDER BY last_name"""
        text = 'ПОМОГАТОРЫ\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'pips':
        """Отправка списка ПиПов по команде ."""
        sql = "SELECT uid, last_name, first_name FROM pips ORDER BY last_name"
        text = 'ПиПы\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'interns':
        """Отправка списка стажеров по команде ."""
        sql = "SELECT uid, last_name, first_name FROM staff WHERE department=3 ORDER BY last_name"
        text = 'СТАЖЕРЫ\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'oos':
        """Отправка списка ОО по команде ."""
        sql = "SELECT uid, last_name, first_name FROM staff WHERE department=4 ORDER BY last_name"
        text = 'ОО\n'
        send_members_list(bot, call.from_user.id, call.message.message_id, sql, text)

    elif call.data == 'test':
        bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text="Все ОК! Твой UID = {}".format(call.from_user.id))

    # elif call.data == 'about':
    #     kbrd = types.InlineKeyboardMarkup()
    #     about_btn = types.InlineKeyboardButton(
    #             text="Сервис отзыва.",
    #             url='')
    #     kbrd.row(about_btn)
    #     bot.edit_message_text(
    #             chat_id=call.from_user.id,
    #             message_id=call.message.message_id,
    #             text='@fancyAndBeauty - Переписал бота и дописываю его при появлении новых идей.'\
    #                 '\nГенерируем идеи.',
    #             reply_markup=kbrd)
                
