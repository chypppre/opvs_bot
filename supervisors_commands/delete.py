import sqlite3

from misc import DB_DIR


def delete(bot, call):
    """Выполнить комманду по кнопке Удалить"""
    if call.data == "delete":
        db = sqlite3.connect(DB_DIR)
        cursor = db.cursor()
        department, uid = call.message.text.split(" ")[:2]
        try:
            if department == "Консультант":
                sql = "DELETE FROM staff WHERE uid={}".format(uid)
            elif department == "Помогатор":
                sql = "DELETE FROM helpers WHERE uid={}".format(uid)
            elif department == "Супервизор":
                sql = "DELETE FROM supers WHERE uid={}".format(uid)
            elif department == "ОО":
                sql = "DELETE FROM staff WHERE uid={}".format(uid)
            elif department == "ПиП":
                sql = "DELETE FROM pips WHERE uid={}".format(uid)
            cursor.execute(sql)
        except Exception as e:
            bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Что-то пошло не так...\n{}".format(e))
            return 0
            
        db.commit()
        cursor.close()
        db.close()
        bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text="Успешно удален.")
