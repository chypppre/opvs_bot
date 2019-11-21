import sqlite3

from telebot import types

from misc import DB_DIR, CHATS_ID


def add_to_tempo(uid, last_name, first_name, department):
    """Добавить во временную таблицу в БД"""
    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()
    check_sql = "SELECT uid FROM tempo WHERE uid={}".format(uid)
    cursor.execute(check_sql)
    if len(cursor.fetchall()) == 1:
        add_sql = "UPDATE tempo SET uid={}, last_name='{}', first_name='{}', department={}".format(
                uid, last_name, first_name, department)
    else:
        add_sql = "INSERT INTO tempo VALUES ({}, '{}', '{}', {})".format(uid, last_name, first_name, department)
    cursor.execute(add_sql)
    db.commit()


def send_add_request(bot, uid):
    """Отправить запрос с данными в бота"""
    kbrd = types.InlineKeyboardMarkup()
    uc_btn = types.InlineKeyboardButton(text="УЦ", callback_data="add_uc")
    uc_helper_btn = types.InlineKeyboardButton(text="Пом.УЦ", callback_data="add_uc_helper")
    uc_super_btn = types.InlineKeyboardButton(text="Супер.УЦ", callback_data="add_uc_super")
    kb_btn = types.InlineKeyboardButton(text="КБухглатерия", callback_data="add_kb")
    kb_helper_btn = types.InlineKeyboardButton(text="Пом.КБухглатерия", callback_data="add_kb_helper")
    kb_super_btn = types.InlineKeyboardButton(text="Супер.КБухглатерия", callback_data="add_kb_super")
    elba_btn = types.InlineKeyboardButton(text="Эльба", callback_data="add_elba")
    elba_helper_btn = types.InlineKeyboardButton(text="Пом.Эльба", callback_data="add_elba_helper")
    elba_super_btn = types.InlineKeyboardButton(text="Супер.Эльба", callback_data="add_elba_super")
    # fms_btn = types.InlineKeyboardButton(text="ФМС", callback_data="add_fms")
    # fms_helper_btn = types.InlineKeyboardButton(text="Пом.ФМС", callback_data="add_fms_helper")
    # fms_super_btn = types.InlineKeyboardButton(text="Супер.ФМС", callback_data="add_fms_super")
    intern_btn = types.InlineKeyboardButton(text="Стажер", callback_data="add_intern")
    mentor_btn = types.InlineKeyboardButton(text="Наставник", callback_data="add_intern_helper")
    oo_btn = types.InlineKeyboardButton(text="ОО", callback_data="add_oo")
    pip_btn = types.InlineKeyboardButton(text="ПиП", callback_data="add_pip")
    decline_btn = types.InlineKeyboardButton(text="Отклонить", callback_data="decline")
    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()
    sql = "SELECT uid, last_name, first_name, department FROM tempo WHERE uid={}".format(uid)
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    uid, last_name, first_name, department= data[0], data[1], data[2], data[3]
    if department in [1,3]:
        chat_id = CHATS_ID[0]
        kbrd.row(uc_btn, uc_helper_btn, uc_super_btn)
        kbrd.row(intern_btn, mentor_btn)
        kbrd.row(oo_btn, pip_btn)
    elif department == 5:
        chat_id = CHATS_ID[6]
        kbrd.row(kb_btn, kb_helper_btn, kb_super_btn)
    elif department == 6:
        chat_id = CHATS_ID[7]
        kbrd.row(elba_btn, elba_helper_btn, elba_super_btn) 
    kbrd.row(decline_btn)
    full_name = "{} {}".format(
            last_name,
            first_name)
    text_for_admins = "{} просит добавить его в бота.\nUID = {}.".format(
            full_name,
            uid)
    bot.send_message(
            chat_id=chat_id,
            text=text_for_admins,
            reply_markup=kbrd)
    

def add_user(bot, call):
    """Добавить юзера согласно нажатой кнопки"""
    text = call.message.text
    text = text.split(" ")
    cons_last_name, cons_first_name, uid = text[0], text[1], text[-1]
    cons_full_name = "{} {}".format(cons_last_name, cons_first_name)
    
    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()

    try:
        if call.data == "add_uc":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                    VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
            cursor.execute(sql) 
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет'.")
        
        elif call.data == "add_kb":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                    VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
            cursor.execute(sql) 
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб, ххх кабинет'.")

        elif call.data == "add_elba":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                    VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
            cursor.execute(sql) 
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб, ххх кабинет'.")

        # elif call.data == "add_fms":
        #     sql = """INSERT INTO staff (uid, department, last_name, first_name)
        #             VALUES ({}, 2, '{}', '{}')""".format(uid, last_name, first_name)
        
        elif call.data == "add_intern":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                    VALUES ({}, 3, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
            cursor.execute(sql)
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Набор дд.мм ххх кабинет'.")
        
        elif call.data == "add_uc_helper":
            try:
                sql = """INSERT INTO helpers (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет' и "\
                    "Установить помогаторский адрес Екб/Влг, ххх кабинет'.")

        elif call.data == "add_kb_helper":
            try:
                sql = """INSERT INTO helpers (uid, department, last_name, first_name)
                        VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб, ххх кабинет' и "\
                    "Установить помогаторский адрес Екб, ххх кабинет'.")

        elif call.data == "add_elba_helper":
            try:
                sql = """INSERT INTO helpers (uid, department, last_name, first_name)
                        VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб, ххх кабинет' и "\
                    "Установить помогаторский адрес Екб, ххх кабинет'.")
        
        # elif call.data == "add_fms_helper":
        #     sql = """INSERT INTO helpers (uid, department, last_name, first_name)
        #             VALUES ({}, 2, '{}', '{}')""".format(uid, last_name, first_name)
        #     cursor.execute(sql)
        #     sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
        #             VALUES ({}, 2, '{}', '{}')""".format(uid, last_name, first_name)
        #     cursor.execute(sql2)
        
        elif call.data == "add_intern_helper":
            try:
                sql2 = """INSERT INTO helpers (uid, department, last_name, first_name)
                        VALUES ({}, 3, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql2)
                sql = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql) 
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет' и "\
                    "Установить помогаторский адрес Екб/Влг, ххх кабинет'.")
        
        elif call.data == "add_uc_super":
            try:
                sql = """INSERT INTO supers (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет' и "\
                    "Установить супервизорский адрес Екб/Влг, ххх кабинет'.") 

        elif call.data == "add_kb_super":
            try:
                sql = """INSERT INTO supers (uid, department, last_name, first_name)
                        VALUES ({}, {}}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет' и "\
                    "Установить супервизорский адрес Екб/Влг, ххх кабинет'.")     

        elif call.data == "add_elba_super":
            try:
                sql = """INSERT INTO supers (uid, department, last_name, first_name)
                        VALUES ({}, {}, '{}', '{}')""".format(uid, department, cons_last_name, cons_first_name)
                cursor.execute(sql)
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 1, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
                cursor.execute(sql2)
            except:
                pass
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет' и "\
                    "Установить супервизорский адрес Екб/Влг, ххх кабинет'.")
            
        # elif call.data == "add_fms_super":
        #     sql = """INSERT INTO supers (uid, department, last_name, first_name)
        #             VALUES ({}, 2, '{}', '{}')""".format(uid, last_name, first_name)
        
        elif call.data == "add_oo":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 4, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
            cursor.execute(sql)
            bot.send_message(
                    chat_id=uid,
                    text="Тебя добавили. Для налача работы напиши боту 'Установить адрес Екб/Влг, ххх кабинет'.")
        
        elif call.data == "add_pip":
            sql = """INSERT INTO staff (uid, department, last_name, first_name)
                    VALUES ({}, 5, '{}', '{}')""".format(uid, cons_last_name, cons_first_name)
            cursor.execute(sql)

    except Exception as e:
        bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Скорее всего пользователь уже добавлен, но вот ошибка\n{}".format(e))

    who_sql = "SELECT last_name, first_name FROM supers WHERE uid={}".format(call.from_user.id)
    cursor.execute(who_sql)
    resp = cursor.fetchall()[0]
    responser_full_name = "{} {} (@{})".format(resp[0], resp[1], call.from_user.username)
    bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="{} успешно добавлен супервизором {}!".format(
                    cons_full_name,
                    responser_full_name))
    delete_sql = "DELETE FROM tempo WHERE uid={}".format(uid)
    cursor.execute(delete_sql)

    db.commit()
    cursor.close()
    db.close()
