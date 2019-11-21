import sqlite3

from telebot import types

from misc import DB_DIR


def delete_user(bot, call):
    """Удалить юзера из БД бота"""
    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()

    if call.data == "delete_cons":
        sql = """SELECT uid, last_name, first_name FROM staff ORDER BY last_name"""
        cursor.execute(sql)
        for uid, last_name, first_name in cursor.fetchall():
            delete_kbrd = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                    text="Удалить",
                    callback_data="delete")
            delete_kbrd.row(btn)
            bot.send_message(
                    chat_id=call.from_user.id,
                    text="Консультант {} {} {}".format(uid, last_name, first_name),
                    reply_markup=delete_kbrd)
    elif call.data == "delete_helper":
        sql = """SELECT uid, last_name, first_name FROM helpers ORDER BY last_name"""
        cursor.execute(sql)
        for uid, last_name, first_name in cursor.fetchall():
            delete_kbrd = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                text="Удалить",
                callback_data="delete")
            delete_kbrd.row(btn)
            bot.send_message(
                chat_id=call.from_user.id,
                text="Помогатор {} {} {}".format(uid, last_name, first_name),
                reply_markup=delete_kbrd)
    elif call.data == "delete_super":
        sql = """SELECT uid, last_name, first_name FROM supers ORDER BY last_name"""
        cursor.execute(sql)
        for uid, last_name, first_name in cursor.fetchall():
            delete_kbrd = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                text="Удалить",
                callback_data="delete")
            delete_kbrd.row(btn)
            bot.send_message(
                chat_id=call.from_user.id,
                text="Супервизор {} {} {}".format(uid, last_name, first_name),
                reply_markup=delete_kbrd)
    elif call.data == "delete_oo":
        sql = """SELECT uid, last_name, first_name FROM staff WHERE department=4 ORDER BY last_name"""
        cursor.execute(sql)
        for uid, last_name, first_name in cursor.fetchall():
            delete_kbrd = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                text="Удалить",
                callback_data="delete")
            delete_kbrd.row(btn)
            bot.send_message(
                chat_id=call.from_user.id,
                text="ОО {} {} {}".format(uid, last_name, first_name),
                reply_markup=delete_kbrd)
    elif call.data == "delete_pip":
        sql = """SELECT uid, last_name, first_name FROM pips ORDER BY last_name"""
        cursor.execute(sql)
        for uid, last_name, first_name in cursor.fetchall():
            delete_kbrd = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                text="Удалить",
                callback_data="delete")
            delete_kbrd.row(btn)
            bot.send_message(
                chat_id=call.from_user.id,
                text="ПиП {} {} {}".format(uid, last_name, first_name),
                reply_markup=delete_kbrd)

    cursor.close()
    db.close()
    