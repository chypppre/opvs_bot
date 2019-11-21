import sqlite3

from telebot import types

from functions import *
from misc import CHATS_ID, DB_DIR


def request_ping(bot, call):
    """Обработка запросов различных пингов"""
    cancel_kbrd = create_keyboard("cancel")  # Делаем клавиатуру для отмены Пинга
    tag = '#ПИНГ'

    cons_uid = call.from_user.id  # Определяем id консультанта
    message_id = call.message.message_id  # Определяем id сообщения

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()

    sql = """SELECT adress, last_name, first_name, ping_status, department
            FROM staff
            WHERE uid={}""".format(cons_uid)
    cursor.execute(sql)
    cons_adress, last_name, first_name, ping_status, cons_department = cursor.fetchall()[0]
    sql2 = """SELECT total_time
            FROM stats
            WHERE department={}""".format(cons_department)
    waiting_time = cursor.execute(sql2).fetchall()[0][0]
    # waiting_time = "{}:{}".format(waiting_time//60, waiting_time%60)
    waiting_time = "-"

    cursor.close()
    db.close()

    if cons_department == 1:
        admin_chat_id = CHATS_ID[0]
    elif cons_department == 2:
        admin_chat_id = CHATS_ID[5]
    elif cons_department == 3:
        admin_chat_id = CHATS_ID[4]
    elif cons_department == 5:
        admin_chat_id = CHATS_ID[6]
    elif cons_department == 6:
        admin_chat_id = CHATS_ID[7]

    user_info = "{} {} (@{})".format(
        first_name,
        last_name,
        call.from_user.username)

    kbrd = types.InlineKeyboardMarkup()

    # Если от консультанта ранее был направлен пинг, то новый пинг не отправляем, пока не ответят на старый
    if ping_status == 1:
        bot.edit_message_text(
                chat_id=cons_uid,
                message_id=message_id,
                text="А-та-та, ожидай пока ответят на предыдущий пинг.")
        return

    # Отправка Продуктового пинга
    elif call.data == "request_ping_product":

        ans_btn = types.InlineKeyboardButton(text="Ответить.", callback_data="response_ping_product")
        kbrd.row(ans_btn)

        if len(cons_adress) > 8:  # Если адрес конс-а записан полностью, то его нужно показать
            super_text = "{} {}\nПришел большущий пинг от {} [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        else:
            super_text = "{}\nПришел большущий пинг от {} [{},{}]".format(tag, user_info, cons_uid, message_id)

        p_type = 'pings'
        cons_text = "Пинг отправлен. Жди теперь ответа. Для отмены пинга тыкай на кнопку."\
                "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "Пингует {}".format(user_info)  # Текст для печати в консоль

    # Отправка пинга по привязке знания
    elif call.data == "request_ping_knowledge":

        ans_btn = types.InlineKeyboardButton(text="Ответить.", callback_data="response_ping_knowledge")
        kbrd.row(ans_btn)

        if len(cons_adress) > 8:  # Если адрес конс-а записан полностью, то его нужно показать
            super_text = "{} {}\n'Непонятно какое знание запилить', говорит {} [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        else:
            super_text = "{}\n'Непонятно какое знание запилить', говорит {} [{},{}]".format(tag, user_info, cons_uid, message_id)

        p_type = 'knowledges'
        cons_text = "Пинг отправлен. Жди теперь ответа. Для отмены пинга тыкай на кнопку."\
                "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "Пингует {}".format(user_info)  # Текст для печати в консоль

    # Проверка заполнения письма/инц-а
    #elif call.data == 'request_ping_check':

    #    ans_btn = types.InlineKeyboardButton(text="Проверить!", callback_data="response_ping_check")
    #    kbrd.row(ans_btn)

    #    if len(cons_adress) > 8:
    #        super_text = "{} {}\n'Проверьте что я тут написакал', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
    #    else:
    #        supeer_text = "{}\n'Проверьте что я тут написакал', говорит {}. [{},{}]".format(tag, user_info, cons_uid, message_id)

    #    p_type = 'checks'
    #    cons_text = "Хатико ждал и ты подожди, пока найдется тот самый. Для отмены пинга тыкай на кнопку."\
    #            "\nПримерное время ожидания ответа {} мин.".format(waiting_time),
    #    console_text = "Граммарнаци = {}".format(user_info)

    # Проверка заполнения письма/инц-а
    #elif call.data == 'request_ping_hard':

    #    ans1_btn = types.InlineKeyboardButton(text="Разрешить.", callback_data="response_ping_hard_yes")
    #    ans2_btn = types.InlineKeyboardButton(text="Не разрешить.", callback_data="response_ping_hard_no")
    #    kbrd.row(ans1_btn)
    #    kbrd.row(ans2_btn)

    #    if len(cons_adress) > 8:
    #        super_text = "{} {}\n'У меня тут сложный инц. Пусти подумоть.', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
    #    else:
    #        super_text = "{}\n'У меня тут сложный инц. Пусти подумоть.', говорит {}. [{},{}]".format(tag, user_info, cons_uid, message_id)

    #    p_type = 'hards'
    #    cons_text = "Хатико ждал и ты подожди, пока найдется тот самый. Для отмены пинга тыкай на кнопку."\
    #            "\nПримерное время ожидания ответа {} мин.".format(waiting_time),
    #    console_text = "Сложный инц у {}".format(user_info)

    # # ПОИСК ЭКСПЕРТА
    # elif call.data == 'request_ping_exp':

    #     if (p_s == 0):
    #         kbrd = types.InlineKeyboardMarkup()
    #         ans_btn = types.InlineKeyboardButton(
    #                 text="Помочь!", callback_data="response_ping_exp_yes")
    #         kbrd.row(ans_btn)

    #         exp_text = "{} {}\n'Тут ну это самое того...', говорит {}. [{},{}]".format(
    #                 tag,
                    # cons_adress,
    #                 user_info,
    #                 cons_uid,
    #                 message_id)
    #         bot.send_message(
    #                 chat_id=CHATS_ID[1],
    #                 text=exp_text,
    #                 reply_markup=kbrd)

    #         is_today(dep)
    #         update_calls('exps', dep)
    #         update_ping_status(
    #                 cons_uid,
    #                 message_id,
    #                 'exp',
    #                 1)

    #         bot.edit_message_text(
    #                 chat_id=call.from_user.id,
    #                 message_id=call.message.message_id,
    #                 text="Ищу эксперта. [Тут картинка Ждуна.] Для отмены пинга тыкай на кнопку.",
    #                 reply_markup=cancel_kbrd)

    #         text = "Жаждет эксперта {}".format(user_info)

    #         print_in_console(
    #                 text=text,
    #                 date=datetime.datetime.now(), fullname="")

    # # УД С ЭКСПЕРТОМ
    # elif call.data == 'request_ping_exp_ud':

    #     if (p_s == 0):

    #         kbrd = types.InlineKeyboardMarkup()
    #         ans1_btn = types.InlineKeyboardButton(
    #                 text="УД :)", callback_data="response_ping_exp_ud_yes")
    #         ans2_btn = types.InlineKeyboardButton(
    #                 text="НеУД :(", callback_data="response_ping_exp_ud_no")
    #         kbrd.row(ans1_btn)
    #         kbrd.row(ans2_btn)

    #         exp_text = "{}\n'Тут так интересно! Ты только глянь!!!', говорит {}. [{},{}]".format(
    #                 tag,
    #                 adress,
    #                 user_info,
    #                 uuid,
    #                 call.message.message_id)
    #         bot.send_message(
    #                 chat_id=CHATS_ID[1],
    #                 text=exp_text,
    #                 reply_markup=kbrd)

    #         is_today(dep)
    #         update_calls('exps', dep)
    #         update_ping_status(
    #                 uuid,
    #                 call.message.message_id,
    #                 'exp',
    #                 1)

    #         bot.edit_message_text(
    #                 chat_id=uuid,
    #                 message_id=call.message.message_id,
    #                 text="Ищу эксперта. [Тут картинка Ждуна.] Для отмены пинга тыкай на кнопку.",
    #                 reply_markup=cancel_kbrd)

    #         text = "Жаждет эксперта на УД {}".format(user_info)

    #         print_in_console(
    #                 text=text,
    #                 date=datetime.datetime.now(), fullname="")

    is_today(cons_department)
    update_calls(p_type, cons_department)
    update_ping_status(cons_uid, message_id, p_type, 1, False)

    bot.send_message(
        chat_id=admin_chat_id,
        text=super_text,
        reply_markup=kbrd)

    bot.edit_message_text(
        chat_id=cons_uid,
        message_id=message_id,
        text=cons_text,
        reply_markup=cancel_kbrd)

    print_in_console(
        text=console_text,
        date=datetime.datetime.now(), fullname="")
