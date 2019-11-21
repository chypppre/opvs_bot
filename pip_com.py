import sqlite3

from telebot import types

from misc import CHATS_ID, DB_DIR
from functions import is_pip, is_mentor, create_keyboard, is_today, update_calls, get_department

# ----------------------------------------------------------------------------
# ---------------------------Проверка и Прослушка-----------------------------
# ----------------------------------------------------------------------------

def pip_com(bot, message):

    uid = message.from_user.id
    if is_pip(uid) or is_mentor(uid):

        db = sqlite3.connect(DB_DIR)
        cursor = db.cursor()

        if is_pip(uid):
            sql = "SELECT last_name, first_name FROM pips WHERE uid={}".format(uid)
            cursor.execute(sql)
            full_name = cursor.fetchall()[0]
            dep = get_department("pips", uid)
        else:
            sql = "SELECT last_name, first_name FROM mentors WHERE uid={}".format(uid)
            cursor.execute(sql)
            full_name = cursor.fetchall()[0]        
            dep = get_department("mentors", uid)
        last_name, first_name = full_name[0], full_name[1]

        full_name = "{} {} (@{})".format(
                last_name,
                first_name,
                message.from_user.username)

        kbrd = create_keyboard(dep)

        # ВИЗИЯ

        if (message.chat.id not in CHATS_ID) \
                and (message.text.lower().startswith("визия")):

            is_today(dep)
            update_calls('visions', dep)

            pip = types.InlineKeyboardMarkup()
            yes = types.InlineKeyboardButton(
                    text = "Отпустить", callback_data = "response_dezh_pip_yes")
            no = types.InlineKeyboardButton(
                    text = "Отказать", callback_data = "response_dezh_pip_no")
            pip.row(yes)
            pip.row(no)
            request_text = 'Отпустите на супервизию {}, - просит {}. [{},{}]'.format(
                            message.text[6:],
                            full_name,
                            str(message.chat.id),
                            str(message.message_id))

            if dep in [1, 3]:
                bot.send_message(
                        chat_id=CHATS_ID[0],
                        text=request_text ,
                        reply_markup = pip)
            elif dep == 2:
                bot.send_message(
                        chat_id=CHATS_ID[5],
                        text=request_text ,
                        reply_markup = pip)
            
            bot.send_message(
                    chat_id=message.from_user.id,
                    text='Запрос на супервизию отправлен, '\
                            'ожидайте ответа, пожалуйста.',
                    reply_markup=kbrd)

        # ПЗ

        elif message.chat.id not in CHATS_ID \
                and (message.text.lower().startswith("пз")):

            is_today(dep)
            update_calls('pzs', dep)

            pip = types.InlineKeyboardMarkup()
            yes = types.InlineKeyboardButton(
                    text = "Отпустить", callback_data = "response_dezh_pip_pz_yes")
            no = types.InlineKeyboardButton(
                    text = "Отказать", callback_data = "response_dezh_pip_pz_no")
            pip.row(yes)
            pip.row(no)
            request_text = 'Отпустите на проверку знаний {}, - просит {}. [{},{}]'.format(
                            message.text[3:],
                            full_name,
                            str(message.chat.id),
                            str(message.message_id))

            if dep == 1:
                bot.send_message(
                        chat_id=CHATS_ID[0],
                        text=request_text ,
                        reply_markup = pip)
            elif dep == 2:
                bot.send_message(
                        chat_id=CHATS_ID[5],
                        text=request_text ,
                        reply_markup = pip)
                
            bot.send_message(
                    chat_id=message.from_user.id,
                    text='Запрос на проверку знаний отправлен, '\
                            'ожидайте ответа, пожалуйста.',
                    reply_markup=kbrd)
