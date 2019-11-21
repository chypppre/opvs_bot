import sqlite3

from misc import DB_DIR


def cancel_logic(bot, call):
    # Отмена пинга
    if call.data == "cancel":
        mydb = sqlite3.connect(DB_DIR)
        cursor = mydb.cursor()
        sql = """UPDATE staff
                SET last_ping_mid=-1, ping_type='empty', ping_status=0, time_to_answer=0
                WHERE uid={}""".format(call.from_user.id)
        cursor.execute(sql)
        sql2 = "SELECT pings_canceled, department FROM staff WHERE uid={}".format(call.from_user.id)
        cursor.execute(sql2)
        data = cursor.fetchall()
        value, dep = data[0][0] + 1, data[0][1]
        sql3 = "UPDATE staff SET pings_canceled={} WHERE uid={}".format(value, call.from_user.id)
        cursor.execute(sql3)
        sql4 = "SELECT pings_canceled FROM stats WHERE department={}".format(dep)
        cursor.execute(sql4)
        data = cursor.fetchall()
        value = data[0][0] + 1
        sql5 = "UPDATE stats SET pings_canceled={} WHERE department={}".format(value, dep)
        cursor.execute(sql5)
        mydb.commit()
        bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text="Пинг отменен.")

    # Отмена пинга дежурного
    elif call.data == "dezh_cancel":
        mydb = sqlite3.connect(DB_DIR)
        cursor = mydb.cursor()
        sql2 = "SELECT dezh_canceled, department FROM staff WHERE uid={}".format(call.from_user.id)
        cursor.execute(sql2)
        data = cursor.fetchall()
        value, dep = data[0][0] + 1, data[0][1]
        sql3 = """UPDATE staff 
                SET dezh_status=0, last_dezh_mid=-1, dezh_canceled={}, time_to_answer_dezh=0
                WHERE uid={}""".format(value, call.from_user.id)
        cursor.execute(sql3)
        sql4 = "SELECT dezh_canceled FROM stats WHERE department={}".format(dep)
        cursor.execute(sql4)
        data = cursor.fetchall()
        value = data[0][0] + 1
        sql5 = "UPDATE stats SET dezh_canceled={} WHERE department={}".format(value, dep)
        cursor.execute(sql5)
        mydb.commit()

        bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text="Пинг дежурки отменен.")
