import sqlite3
import re

from functions import *
from misc import DB_DIR, CHATS_ID

def response_dezh(bot, call):

    text = call.message.text
    r = re.compile(r'\d+,\d+')
    cons_uid, cons_message_id = r.findall(text)[0].split(",")
    username = re.compile(r'@[a-zA-Z0-9_]+')
    cons_username = username.findall(text)[0]

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()
    sql = """SELECT adress, last_name, first_name, dezh_status, last_dezh_mid
            FROM staff 
            WHERE uid={}""".format(cons_uid)
    cursor.execute(sql)
    cons_adress, cons_last_name, cons_first_name, dezh_status, last_dezh_mid = cursor.fetchall()[0]
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

    sql = "SELECT adress, last_name, first_name FROM {} WHERE uid={}".format(table_name, responser_uid)
    cursor.execute(sql)
    responser_adress, responser_last_name, responser_first_name = cursor.fetchall()[0]  # Рабочий адрес ответившего
    responser_full_name = "{} {} (@{})".format(  # Фамилия имя ник ответившего на пинг
            responser_last_name,
            responser_first_name,
            call.from_user.username)

    cursor.close()
    db.close()

    # ОТВЕТы ДЕЖУРКИ

    # -------------------------------- ПиПы, ПЗ, Визия ------------------------------------
    if call.data == "response_dezh_pip_yes" :
        if is_super(call.from_user.id):
            # Ответ на супервизию
            cons_full_name = call.message.text[len("Отпустите на супервизию "): \
                                          call.message.text.index(',')]
            who_calling = call.message.text[call.message.text.index('просит ') + 7: \
                                            call.message.text.index('.')]
            bot.send_message(
                    chat_id=cons_uid,
                    text="{} разрешил {} пойти на визию.".format(
                            responser_full_name, 
                            cons_full_name))
            try:
                positive_answer_text = '{} разрешил провести супервизию {} c {}.'.format(
                        responser_full_name,
                        who_calling, 
                        cons_full_name)
                bot.edit_message_text(
                        chat_id=admin_chat_id,
                        message_id=call.message.message_id,
                        text=positive_answer_text)
            except Exception as e:
                print("IN response dezh pip \n{}".format(e))

            is_today(department)
            update_answers(call.from_user.id, 'visions')

            pip_yes_text = "Визия одобрена от {}\n".format(responser_full_name)
            print_in_console(
                text=pip_yes_text,
                date=datetime.datetime.now(), fullname="")
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, у тебя не хватает скилла. Оставь это супервизору.".format(responser_full_name))

    elif call.data == "response_dezh_pip_no":

        if is_super(call.from_user.id):
            cons_full_name = call.message.text[len("Отпустите на супервизию "): \
                                          call.message.text.index(',')]
            who_calling = call.message.text[call.message.text.index('просит ') + 7: \
                                            call.message.text.index('.')]
            bot.send_message(
                chat_id=cons_uid,
                text='Сейчас нет возможности отпустить {} '\
                     'пройти на визию.\nПопробуй позже.'.format(cons_full_name))
            try:
                negative_answer_text = '{} не разрешил провести супервизию {} c {}.'.format(
                        responser_full_name, who_calling, cons_full_name)
                bot.edit_message_text(
                        chat_id=admin_chat_id,
                        message_id=call.message.message_id,
                        text=negative_answer_text)
            except Exception as e:
                print("IN response dezh pip\n{}".format(e))

            is_today(department)
            update_answers(call.from_user.id, 'visions')

            pip_no_text = "Визия отклонена от {}\n".format(responser_full_name)
            print_in_console(
                text=pip_no_text,
                date=datetime.datetime.now(), fullname="")
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, у тебя не хватает скилла. Оставь это супервизору.".format(responser_full_name))

    elif call.data == "response_dezh_pip_pz_yes":

        if is_super(call.from_user.id):
            # Ответ на проверку знаний
            cons_full_name = call.message.text[len("Отпустите на проверку знаний "): \
                                          call.message.text.index(',')]
            who_calling = call.message.text[call.message.text.index('просит ') + 7: \
                                            call.message.text.index('.')]
            bot.send_message(
                    chat_id=cons_uid,
                    text="{} разрешил {} пойти на ПЗ.".format(
                            responser_full_name, cons_full_name))
            try:
                positive_answer_text = '{} разрешил провести проверку знаний {} c {}.'.format(
                        responser_full_name, who_calling, cons_full_name)
                bot.edit_message_text(
                        chat_id=admin_chat_id,
                        message_id=call.message.message_id,
                        text=positive_answer_text)
            except Exception as e:
                print("IN response dezh pz\n{}".format(e))

            is_today(department)
            update_answers(call.from_user.id, 'pzs')

            pip_yes_text = "Проверка знаний одобрена от {}\n".format(responser_full_name)
            print_in_console(
                    text=pip_yes_text,
                    date=datetime.datetime.now(), fullname="")
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, у тебя не хватает скилла. Оставь это супервизору.".format(responser_full_name))

    elif call.data == "response_dezh_pip_pz_no":
        
        if is_super(call.from_user.id):
            # Отказ на проверку знаний
            cons_full_name = call.message.text[len("Отпустите на проверку знаний "): \
                                          call.message.text.index(',')]
            who_calling = call.message.text[call.message.text.index('просит ') + 7: \
                                            call.message.text.index('.')]
            bot.send_message(
                    chat_id=cons_uid,
                    text='Сейчас нет возможности отпустить {} ' \
                         'пройти проверку знаний.\nПопробуй позже.'.format(cons_full_name))
            try:
                negative_answer_text = '{} не разрешил провести проверку знаний {} c {}.'.format(
                        responser_full_name, who_calling, cons_full_name)
                bot.edit_message_text(
                        chat_id=admin_chat_id,
                        message_id=call.message.message_id,
                        text=negative_answer_text)
            except Exception as e:
                print("IN response dezh pz \n{}".format(e))

            is_today(department)
            update_answers(call.from_user.id, 'pzs')

            pip_no_text = "Проверка знаний отклонена от {}\n".format(responser_full_name)
            print_in_console(
                text=pip_no_text,
                date=datetime.datetime.now(), fullname="")
        else:
            bot.send_message(
                    chat_id=admin_chat_id,
                    text="{}, у тебя не хватает скилла. Оставь это супервизору.".format(responser_full_name))
# --------------------------------------------------------------------------------------------------------------------------------------
    else:
        if dezh_status == 0:
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

        elif call.data == "response_dezh_f":
            # Ответ в личку пингующему
            cons_text = '{} ответил, как дежуркa. Я тут: {}.'.format(responser_full_name, responser_adress)
            super_text="{} ответил, как главный дежурк {}.".format(responser_full_name, cons_full_name)
            d_type = 'f_dezh'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_h":
            # Ответ в личку пингующему
            cons_text = '{} ответил, как неглавный дежуркa. Я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} ответил, как неглавный дежурк {}.'.format(responser_full_name, cons_full_name)
            d_type = 'h_dezh'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_break_time":
            # Ответ в личку пингующему
            cons_text = '{} ответил, как дежуркa. Я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} ответил, что разбереться с перерывом у {}.'.format(responser_full_name, cons_full_name)
            d_type = 'break_time'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_reboot_yes":
            # Ответ в личку пингующему
            cons_text = '{} ответил, что можно перезагружать. Если что, я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} одобрил перезагрузку {}.'.format(responser_full_name, cons_full_name)
            d_type = 'reboot_yes'
            console_text = "Ответ получен от {}\n".format(responser_full_name)

        elif call.data == "response_dezh_reboot_no":
            # Ответ в личку пингующему
            cons_text = '{} ответил, что пока нельзя перезагружаться. Если что, я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} отклонил перезагрузку у {}.'.format(responser_full_name, cons_full_name)
            d_type = 'reboot_no'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_op_time":
            # Ответ в личку пингующему
            cons_text = '{} ответил, как дежуркa. Я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} узнает, что там у {} с ОП.'.format(responser_full_name, cons_full_name)
            d_type = 'op_time'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_miss_fix_break":
            # Ответ в личку пингующему
            cons_text = '{} ответил, как дежуркa. Я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} узнает, почему {} пропускает фиксированный перерыв.'.format(responser_full_name, cons_full_name)
            d_type = 'miss'
            console_text = "Ответ получен от {}\n".format(responser_full_name)    
        
        elif call.data == "response_dezh_study_yes":
            # Ответ в личку пингующему
            cons_text = '{} разрешил пойти в обучение/прослушку. Если что, я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} разрешил пойти в обучение/прослушку {}.'.format(responser_full_name, cons_full_name)
            d_type = 'study_yes'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        elif call.data == "response_dezh_study_no":
            # Ответ в личку пингующему
            cons_text = '{} неразрешил пойти в обучение/прослушку. Если что, я тут: {}.'.format(responser_full_name, responser_adress)
            super_text = '{} неразрешил пойти в обучение/прослушку {}.'.format(responser_full_name, cons_full_name)
            d_type = 'study_no'
            console_text = "Ответ получен от {}\n".format(responser_full_name)
            
        is_today(department)
        update_answers(call.from_user.id, d_type, admin_chat_id)
        update_dezh_status(cons_uid, -1, "empty", 0, True)

        bot.send_message(
                chat_id=cons_uid,
                text=cons_text)
        try:
            # Сообщение консультанту
            bot.delete_message(
                    chat_id=cons_uid,
                    message_id=last_dezh_mid)
            # Сообщение в "админский" чат, с именем того, кто взял пингующего на себя.
            bot.edit_message_text(
                    chat_id=admin_chat_id,
                    message_id=call.message.message_id,
                    text=super_text)
        except Exception as e:
            print("IN response dezh\n{}".format(e))

        print_in_console(
            text=console_text,
            date=datetime.datetime.now(), fullname="")
