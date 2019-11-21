import sqlite3

from misc import DB_DIR


def find_cons_logic(bot, message):
    # Найти информацию о пользователе по его фамилии
    if message.text.lower().startswith('найти'):
        text = message.text.split()
        db = sqlite3.connect(DB_DIR)
        mycursor = db.cursor()
        try:
            last_name = text[1]
            sql = """SELECT uid, last_name, first_name
                    FROM staff
                    WHERE last_name='{0}'
                    UNION
                    SELECT uid, last_name, first_name
                    FROM pips
                    WHERE last_name='{0}'
                    UNION
                    SELECT uid, last_name, first_name
                    FROM supers 
                    WHERE last_name='{0}'
                    UNION
                    SELECT uid, last_name, first_name
                    FROM helpers 
                    WHERE last_name='{0}'""".format(last_name)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            uid, last_name, first_name = result[0]
            info = "uid - {}\n"\
                    "Фамилия - {}\n"\
                    "Имя - {}".format(uid, last_name, first_name)
            bot.send_message(
                    chat_id=message.from_user.id,
                    text=info)
            mycursor.close()
        except Exception as e:
            bot.send_message(
                    chat_id=message.from_user.id,
                    text='Пользователь не найден. Корректный пример:'\
                        '\nнайти Фамилия\n'+str(e)) 
