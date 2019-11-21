import sqlite3

from telebot import types

from misc import interns, CHATS_ID, DB_DIR, OO_DIR
from functions import *


# ---------------------------КОМАНДЫ СТАЖЕРОВ-----------------------------
def intern_com(bot, message):

    department = get_department('staff', message.from_user.id)

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()

    sql = """SELECT last_name, first_name, adress, ping_status, dezh_status
            FROM staff
            WHERE uid={}""".format(message.from_user.id)
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    last_name, first_name, adress = data[0], data[1], data[2]
    ping_status, dezh_status = data[3], data[4]

    # ------------------ ПИНГ НАСТАВНИКАМ ----------------
    if message.text == "Пинг" and ping_status == 0:

        keyboard = types.InlineKeyboardMarkup()
        ping_btn = types.InlineKeyboardButton(
            text="Пинг по инцу.", callback_data="request_ping_product")
        knowledge_ping_btn = types.InlineKeyboardButton(
            text="Привязка знания.", callback_data="request_ping_knowledge")
        check_btn = types.InlineKeyboardButton(
            text="Проверить меня.", callback_data="request_ping_check")
        hard_btn = types.InlineKeyboardButton(
            text="Сложный инц.", callback_data="request_ping_hard")
        keyboard.row(ping_btn)
        keyboard.row(knowledge_ping_btn)
        keyboard.row(check_btn)
        keyboard.row(hard_btn)

        bot.send_message(
                chat_id=message.from_user.id,
                text="Выбери тип пинга:",
                reply_markup=keyboard)

    # ------------------ НАСТАВНИКУ - ДЕЖУРКЕ ----------------
    elif message.text == "Дежурный" and dezh_status == 0:

        options_kbrd = types.InlineKeyboardMarkup()
        dezh_btn = types.InlineKeyboardButton(
                text="Прочее", callback_data="request_dezh_other")
        break_btn = types.InlineKeyboardButton(
                text="Перерыв.", callback_data="request_dezh_break_time")
        reboot_btn = types.InlineKeyboardButton(
                text="Дежурный.", callback_data="request_dezh_reboot")
        op_btn = types.InlineKeyboardButton(
                text="Обучение/Самопрослушка.", callback_data="request_dezh_op_time")
        options_kbrd.row(break_btn)
        options_kbrd.row(reboot_btn)
        options_kbrd.row(op_btn)
        options_kbrd.row(dezh_btn)

        # Отправляется сообщение в "Админский чат"
        bot.send_message(
                chat_id=message.from_user.id,
                text="Причина запроса:",
                reply_markup=options_kbrd)

    # Если пинг или дежурка уже были направлены...
    elif ping_status == 1 or dezh_status == 1:
        bot.send_message(
                chat_id=message.from_user.id,
                text="Ты уже отправлял пинг, погоди немного.")

    oo_info(bot, message)
