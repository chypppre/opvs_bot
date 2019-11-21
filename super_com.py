import sqlite3

from telebot import types

from functions import refresh
from misc import supers, DB_DIR

# ---------------------------КОМАНДЫ СУПЕРВИЗОРОВ-----------------------------

def super_com(bot, message):

    # ДОБАВИТЬ ПОЛЬЗОВАТЕЛЕЙ

    mydb = sqlite3.connect(DB_DIR)
    mycursor = mydb.cursor()

    if (message.from_user.id in supers) \
            and (message.text.lower().startswith('добавить массово')):
        text = message.text.split(' ')
        try:
            # добавить массово отдел 1,... Фамилия_Имя,Фамилия_Имя,...
            what, uids, full_names = text[2:]
            uids = uids.split(",")
            full_names = full_names.split(",")

            if what == 'кэ':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql1 = "INSERT INTO staff (uid, department, last_name, first_name) "\
                            "VALUES ({}, 1, '{}', '{}')".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Консультанты успешно добавлены!')
                mycursor.close()

            elif what == 'помкэ':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql1 = "INSERT INTO helpers (uid, department, last_name, first_name) "\
                            "VALUES ({}, 1, '{}', '{}')".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогаторы успешно добавлены!')
                mycursor.close()

            elif what == 'помст':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql1 = "INSERT INTO helpers (uid, department, last_name, first_name) "\
                            "VALUES ({}, 3, '{}', '{}')".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогаторы стажеров успешно добавлены!')
                mycursor.close()

            elif what == 'пип':
                sql1 = """INSERT INTO pips (uid, last_name, first_name)
                        VALUES ({}, '{}', '{}')""".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mycursor = mydb.cursor()
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='ПиПовцы успешно добавлены!')
                mycursor.close()

            elif what == 'оо':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql1 = """INSERT INTO staff (uid, department, last_name, first_name)
                             VALUES ({}, 4, '{}', '{}')""".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Сотрудники ОО успешно добавлены!')
                mycursor.close()

            elif what == 'суперкэ':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql1 = """INSERT INTO supers (uid, department, last_name, first_name)
                             VALUES ({}, 1, '{}', '{}')""".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Супервизоры успешно добавлены!')
                mycursor.close()

            elif what == 'ст':
                for n in range(len(uids)):
                    full_name = full_names[n].split("_")
                    sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                            VALUES ({}, 3, '{}', '{}')""".format(
                                    uids[n], full_name[0], full_name[1])
                    mycursor.execute(sql2)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Стажеры успешно добавлены!')
            refresh()
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text=r'Введены неправильные данные! '\
                    'Корректный пример:\nдобавить к/п/пип/с/ст UID Фамилия Имя\n'+str(e))

    # ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ

    elif (message.from_user.id in supers) \
            and (message.text.lower().startswith('добавить')):
        text = message.text.split(' ')
        try:

            what, uid, last_name, first_name = text[1:]

            if what == 'кэ':
                sql1 = "INSERT INTO staff (uid, department, last_name, first_name) "\
                        "VALUES ({}, 1, '{}', '{}')".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Консультант успешно добавлен!')
                mycursor.close()

            elif what == 'помкэ':
                sql1 = "INSERT INTO helpers (uid, department, last_name, first_name) "\
                        "VALUES ({}, 1, '{}', '{}')".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогатор успешно добавлен!')
                mycursor.close()

            elif what == 'помст':
                sql1 = "INSERT INTO helpers (uid, department, last_name, first_name) "\
                        "VALUES ({}, 3, '{}', '{}')".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогатор успешно добавлен!')
                mycursor.close()

            elif what == 'пип':
                sql1 = """INSERT INTO pips (uid, last_name, first_name)
                        VALUES ({}, '{}', '{}')""".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mycursor = mydb.cursor()
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='ПиПовец успешно добавлен!')
                mycursor.close()

            elif what == 'оо':
                sql1 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 4, '{}', '{}')""".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mycursor = mydb.cursor()
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Сотрудник ОО успешно добавлен!')
                mycursor.close()

            elif what == 'суперкэ':
                sql1 = """INSERT INTO supers (uid, department, last_name, first_name)
                         VALUES ({}, 1, '{}', '{}')""".format(
                                uid, last_name, first_name)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Супервизор успешно добавлен!')
                mycursor.close()

            elif what == 'ст':
                sql2 = """INSERT INTO staff (uid, department, last_name, first_name)
                        VALUES ({}, 3, '{}', '{}')""".format(uid, last_name, first_name)
                mycursor.execute(sql2)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Стажер успешно добавлен!')
            refresh()
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text=r'Введены неправильные данные! '\
                    'Корректный пример:\nдобавить к/п/пип/с/ст UID Фамилия Имя\n'+str(e))

    # УДАЛИТЬ ПОЛЬЗОВАТЕЛЕЙ

    elif (message.from_user.id in supers) \
            and (message.text.lower().startswith('удалить массово')):
        data = message.text.lower()
        try:
            text = message.text.split(' ')
            what, del_uids = text[2:]
            del_uids = del_uids.split(",")

            if what == 'конс':
                for uid in del_uids:
                    for col in ['staff','helpers','supers','pips']:
                        try:
                            sql = "DELETE FROM {} WHERE uid={}".format(col, uid)
                            mycursor.execute(sql)
                        except:
                            pass
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Консультанты успешно удалены!')
                mycursor.close()

            elif what == 'пом':
                for uid in del_uids:
                    sql1 = "DELETE FROM helpers WHERE uid={}".format(uid)
                    mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогаторы успешно удалены!')
                mycursor.close()

            elif what == 'пип':
                for uid in del_uids:
                    sql1 = "DELETE FROM pips WHERE uid={}".format(uid)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='ПиПовецы успешно удалены!')
                mycursor.close()

            elif what == 'супер':
                for uid in del_uids:
                    sql = "DELETE FROM supers WHERE uid={}".format(uid)
                mycursor.execute(sql)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Супервизоры успешно удалены!')
                mycursor.close()

            elif what == 'ст':
                for uid in del_uids:
                    sql = "DELETE FROM staff WHERE uid={}".format(uid)
                mycursor.execute(sql)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Стажеры успешно удалены!')
                mycursor.close()
            refresh()
        except Exception as E:
            bot.send_message(
                    chat_id=message.chat.id,
                    text=r'Введены неправильные данные! '\
                        'Корректный пример: \nудалить к/п/пип/с/ст UID\n'\
                        +str(E))

    # УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ

    elif (message.from_user.id in supers) \
            and (message.text.lower().startswith('удалить')):
        data = message.text.lower()
        try:
            text = message.text.split(' ')
            what, del_uid = text[1:]
            if what == 'конс':
                for col in ['staff','helpers','supers','pips']:
                    try:
                        sql = "DELETE FROM {} WHERE uid={}".format(col, del_uid)
                        mycursor.execute(sql)
                    except:
                        pass
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Консультант успешно удален!')
                mycursor.close()
            elif what == 'пом':
                sql1 = "DELETE FROM helpers WHERE uid={}".format(del_uid)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Помогатор успешно удален!')
                mycursor.close()
            elif what == 'пип':
                sql1 = "DELETE FROM pips WHERE uid={}".format(del_uid)
                mycursor.execute(sql1)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='ПиПовец успешно удален!')
                mycursor.close()
            elif what == 'супер':
                sql = "DELETE FROM supers WHERE uid={}".format(del_uid)
                mycursor.execute(sql)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Супервизор успешно удален!')
                mycursor.close()
            elif what == 'ст':
                sql = "DELETE FROM staff WHERE uid={}".format(del_uid)
                mycursor.execute(sql)
                mydb.commit()
                bot.send_message(
                        chat_id=message.chat.id,
                        text='Стажер успешно удален!')
                mycursor.close()
            refresh()
        except Exception as E:
            bot.send_message(
                    chat_id=message.chat.id,
                    text=r'Введены неправильные данные! '\
                        'Корректный пример: \nудалить к/п/пип/с/ст UID\n'\
                        +str(E))

    # ОБНУЛИТЬ СТАТУ

    elif (message.from_user.id in supers) \
            and (message.text.lower().startswith('обнулить')):
        text = message.text.split()
        try:
            uid = text[1]
            sql = """UPDATE staff
                    SET last_ping_mid=-1, ping_type='empty', ping_status=0, dezh_status=0
                    WHERE uid={}""".format(uid)
            mycursor.execute(sql)
            mycursor.close()
            mydb.commit()
            bot.send_message(
                    chat_id=message.from_user.id,
                    text="Успешно")
        except Exception as e:
            bot.send_message(
                    chat_id=message.from_user.id,
                    text=str(e))

    # СМЕНИТЬ ОТДЕЛ

    elif (message.from_user.id in supers) \
            and (message.text == 'сменить'):
        text = message.text.split()
        try:
            uid, dep = text[1:]
            sql = """UPDATE staff
                    SET department={}
                    WHERE uid={}""".format(dep, uid)
            mycursor.execute(sql)
            mycursor.close()
            mydb.commit()
            bot.send_message(
                    chat_id=message.from_user.id,
                    text="Успешно")
        except Exception as e:
            bot.send_message(
                    chat_id=message.from_user.id,
                    text=str(e))
