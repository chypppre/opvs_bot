import re
import sqlite3

from telebot import types

from functions import *
from misc import DB_DIR, CHATS_ID


def response_ping(bot, call):

    text = call.message.text
    r = re.compile(r'\d+,\d+')
    cons_uid, cons_message_id = r.findall(text)[0].split(",")
    username = re.compile(r'@[a-zA-Z0-9_]+')
    cons_username = username.findall(text)[0]

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()
    sql = """SELECT adress, last_name, first_name, ping_status, last_ping_mid
            FROM staff 
            WHERE uid={}""".format(cons_uid)
    cursor.execute(sql)
    cons_adress, cons_last_name, cons_first_name, ping_status, last_ping_mid = cursor.fetchall()[0]
    cons_full_name = "{} {} ({})".format(  # Фамилия имя ник отправившего пинг
            cons_last_name,
            cons_first_name,
            cons_username)

    admin_chat_id = call.message.chat.id      
    responser_uid = call.from_user.id
    if is_mentor(responser_uid) and admin_chat_id == CHATS_ID[4]:
        table_name = 'mentors'
        department = get_department('mentors', responser_uid)
    elif is_helper(responser_uid):
        table_name = 'helpers'
        department = get_department('helpers', responser_uid)
    elif is_super(responser_uid):
        table_name = "supers"
        department = get_department('supers', responser_uid)

    sql = "SELECT last_name, first_name, adress FROM {} WHERE uid={}".format(table_name, responser_uid)
    cursor.execute(sql)
    responser_last_name, responser_first_name, responser_adress = cursor.fetchall()[0]  # Рабочий адрес ответившего
    responser_full_name = "{} {} (@{})".format(  # Фамилия имя ник ответившего на пинг
            responser_last_name,
            responser_first_name,
            call.from_user.username)

    cursor.close()
    db.close()

    # Если пинг неактуален (Статус = 0), то закрываем лавочку
    if ping_status == 0:
        text = call.message.text
        cons_pat = re.compile(r'[а-яА-ЯёЁ]+ [а-яА-ЯёЁ]+ [(@].+[)]')
        cons = cons_pat.findall(text)[0]
        try:
            bot.edit_message_text(
                chat_id=admin_chat_id,
                message_id=call.message.message_id,
                text="Пинг уже неактуален.\nОтменил {}.".format(cons))
        except Exception as e:
            print("IN CALLBACK_COM ping\n{}".format(e))
        return

    # Иначе, если статус != 0, то отвечаем
    # Ответ на продуктовый пинг
    elif call.data == "response_ping_product":
        cons_text = '{} ответил на твой пинг.'\
                ' Я тут: {}. Если ты не задашь вопрос в течение 2-х минут, '\
                'то я пойду помогать другому консультанту.'.format(
                        responser_full_name,
                        responser_adress)
        super_text = "{} ответил на пинг {}.".format(responser_full_name, cons_full_name)
        p_type = 'pings'
        console_text = "Ответ получен от {}\n".format(responser_full_name)
    
    # Ответ на пинг по привязке знания
    elif call.data == "response_ping_knowledge":
        cons_text = '{} ответил на твой пинг.'\
                ' Я тут: {}. Если ты не задашь вопрос в течение 2-х минут, '\
                'то я пойду помогать другому консультанту.'.format(
                        responser_full_name,
                        responser_adress)
        super_text="{} ответил на пинг {}.".format(responser_full_name, cons_full_name)
        p_type = 'knowledges'
        console_text = "Ответ получен от {}\n".format(responser_full_name)

    # ОТВЕТ НА ПОИСК ЗАЯВКУ
    elif call.data == 'response_ping_lost':
        if is_super(responser_uid):
            # Ответ в личку пингующему
            cons_text = "{} ответил, что готов к поиску этой заявки. Найти меня можно: {}.".format(
                    responser_full_name,
                    responser_adress)
            super_text = "{} ответил {}, что охота на заявку открыта.".format(responser_full_name, cons_full_name)
            p_type = 'losts'
            console_text = "Охота открыта от {}\n".format(responser_full_name)
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, тебе не хватает скила, ответить может только супервизор.".format(responser_full_name))

    # ОТВЕТ КЦР
    elif call.data == 'response_ping_kcr':
        if is_super(responser_uid):
            cons_text = "{} ответил что пойдет разбираться с клятi КЦР. Найти меня можно: {}.".format(
                            responser_full_name,
                            responser_adress)
            super_text = "{} ответил {}, что пойдет разбираться с клятi КЦР.".format(responser_full_name, cons_full_name)
            p_type = 'kcrs'
            console_text = "КЦР разобран {}\n".format(responser_full_name)
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, тебе не хватает скила, ответить может только супервизор.".format(responser_full_name))

    # ОТВЕТ на проверку письма или инц-а
    elif call.data == 'response_ping_check':        
        cons_text = "{} ответил что пойдет проверить что у тебя написано. Найти меня можно: {}.".format(
                        responser_full_name,
                        responser_adress)
        super_text = "{} ответил {}, что является граммарнаци и уже вышел.".format(responser_full_name, cons_full_name)
        p_type = 'checks'
        console_text = "Безграмотный обезврежен {}\n".format(responser_full_name)
        
    # ОТВЕТ на просьбу о сложном инце
    elif call.data == 'response_ping_hard_yes':        
        cons_text = "{} ответил что разрешил пойти в сложный. Найти меня можно: {}.".format(
                        responser_full_name,
                        responser_adress)
        super_text = "{} разрешил {} пойти в сложный.".format(responser_full_name, cons_full_name)
        p_type = 'hards_yes'
        console_text = "Сложный инц локализован {}\n".format(responser_full_name)
        
    # ОТВЕТ на просьбу о сложном инце
    elif call.data == 'response_ping_hard_no':        
        cons_text = "{} ответил что нельзя пойти в сложный. Найти меня можно: {}.".format(
                        responser_full_name,
                        responser_adress)
        super_text = "{} не разрешил {} пойти в сложный.".format(responser_full_name, cons_full_name)
        p_type = 'hards_no'
        console_text = "Сложный инц решается в рабочее время {}\n".format(responser_full_name)
        
    # # ОТВЕТ НА ПОИСК ЭКСПЕРТА
    # elif call.data == 'response_ping_exp_yes':
#         exp_text = "{} {} (@{}) думает, что сможет помочь тебе.".format(
#                 str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username))

#         bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=last_ping_mid,
#                 text=exp_text)
#         # Сообщение в "админский" чат, с именем того, кто взял пингующего на себя.
#         try:
#             exp_chat_text = '{} {} (@{}) ответил {}, что жизненные'\
#                     ' трудности и препятствия делают нас только сильнее и сейчас разберется.'.format\
#                 (str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username),
#                 full_name)

#             bot.edit_message_text(
#                     chat_id=CHATS_ID[1],
#                     message_id=call.message.message_id,
#                     text=exp_chat_text)
#         except Exception as e:
#             print("IN CALLBACK_COM 883 \n{}".format(e))

#         # update_answers(call.from_user.id, exp)
#         update_ping_status(
#                 chat_id,
#                 -1,
#                 'empty',
#                 0)

#         exp_console_text = "Эксперт призван {} {} (@{})\n".format(
#                 str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username))

#         print_in_console(
#                 text=exp_console_text,
#                 date=datetime.datetime.now(), fullname="")

    # #ЭКСПЕРТЫ С УД

    # elif call.data == 'response_ping_exp_ud_yes':
#         exp_text = "{} {} (@{}) щас покажет как это там делается, ага, ага!.".format(
#                 str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username))

#         bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=last_ping_mid,
#                 text=exp_text)
#         # Сообщение в "админский" чат, с именем того, кто взял пингующего на себя.
#         try:
#             exp_chat_text = '{} {} (@{}) ответил {}, что УД бояться -'\
#                     ' в УКС не работать и сейчас все починит.'.format\
#                 (str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username),
#                 full_name)

#             bot.edit_message_text(
#                     chat_id=CHATS_ID[1],
#                     message_id=call.message.message_id,
#                     text=exp_chat_text)
#         except Exception as e:
#             print("IN CALLBACK_COM 942 \n{}".format(e))

#         # update_answers(call.from_user.id, exp)
#         update_ping_status(
#                 chat_id,
#                 -1,
#                 'empty',
#                 0)

#         exp_console_text = "Эксперт призван {} {} (@{})\n".format(
#                 str(call.from_user.first_name),
#                 str(call.from_user.last_name),
#                 str(call.from_user.username))

#         print_in_console(
#                 text=exp_console_text,
#                 date=datetime.datetime.now(), fullname="")

    # elif call.data == 'response_ping_exp_ud_no':

        # exp_text = "{} {} (@{}) решит легко, но не сегодня... Увы и ах!".format(
        #         str(call.from_user.first_name),
        #         str(call.from_user.last_name),
        #         str(call.from_user.username))
        # bot.send_message(
        #         chat_id=chat_id,
        #         text=exp_text)
        # # Сообщение в "админский" чат, с именем того, кто взял пингующего на себя.
        # try:
        #     exp_chat_text = '{} ответил {}, что УД, конечно,'\
        #             ' интересно, но сейчас завал и вообще "Ой, всё".'.format(
        #                     responser_full_name,
        #                     cons_full_name)
        #
        #     bot.edit_message_text(
        #             chat_id=CHATS_ID[1],
        #             message_id=call.message.message_id,
        #             text=exp_chat_text)
        # except Exception as e:
        #     print("IN CALLBACK_COM exp_ud \n{}".format(e))
        #
        # # update_answers(call.from_user.id, exp)
        # update_ping_status(
        #         cons_uid,
        #         -1,
        #         'empty',
        #         0)
        #
        # exp_console_text = "Эксперт призван {}\n".format(responser_full_name)
        # print_in_console(
        #         text=exp_console_text,
        #         date=datetime.datetime.now(), fullname="")

    is_today(department)
    update_answers(call.from_user.id, p_type, admin_chat_id)
    update_ping_status(cons_uid, -1, 'empty', 0, True)

    bot.send_message(  # Сообщение в чат пингующему
            chat_id=cons_uid,
            text=cons_text)
    try:
        bot.delete_message(  # Удаление сообщения с "Отменой" в чате консультанта
                chat_id=cons_uid,
                message_id=last_ping_mid)
    except:
        if ping_status == 1:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="Что-то пошло не так, но консультант {} получил ответ. "\
                    "Не обращайте внимание".format(cons_full_name))

    # Сообщение в "админский" чат, с именем того, кто взял пингующего на себя. call.message.chat.id
    try:
        bot.edit_message_text(
                chat_id=admin_chat_id,
                message_id=call.message.message_id,
                text=super_text)
    except Exception as e:
        print("IN response_ping ping\n{}".format(e))

    print_in_console(
            text=console_text,
            date=datetime.datetime.now(), fullname="")