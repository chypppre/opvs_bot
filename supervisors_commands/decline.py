import sqlite3

from misc import DB_DIR


def decline_logic(bot, call, uid):
	# Отказать в заселении в БД Бота
    
    text = call.message.text
    text = text.split(" ")

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()
    sql = "SELECT last_name, first_name FROM supers WHERE uid={}".format(call.from_user.id)
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    responser_full_name = "{} {} (@{})".format(data[0], data[1], call.from_user.username)
    
    cons_full_name = "{} {}".format(text[0], text[1])
    cons_uid = text[-1]

    bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="{} отклонил заявку на добавление {}.". format(
                    responser_full_name,
                    cons_full_name))

    bot.send_message(
            chat_id=cons_uid,
            text="Тебе отказали в добавлении. Напиши @{}, чтобы узнать причину.".format(call.from_user.username))
    delete_sql = "DELETE FROM tempo WHERE uid={}".format(cons_uid)
    cursor.execute(delete_sql)
    db.commit()
    cursor.close()
    db.close()
