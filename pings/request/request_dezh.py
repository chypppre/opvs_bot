import sqlite3

from telebot import types

from functions import *
from misc import DB_DIR, CHATS_ID


def request_dezh(bot, call):
    """Обработка запросов для дежурного"""
    dezh_cancel_kbrd = create_keyboard("dezh_cancel")  # Делаем клавиатуру для отмены Пинга дежурного
    tag = '#ДЕЖУРНЫЙ'

    cons_uid = call.from_user.id  # Определяем id консультанта
    message_id = call.message.message_id  # Определяем id сообщения

    db = sqlite3.connect(DB_DIR)
    cursor = db.cursor()

    sql = """SELECT adress, last_name, first_name, dezh_status, department
            FROM staff
            WHERE uid={}""".format(cons_uid)
    cursor.execute(sql)
    cons_adress, last_name, first_name, dezh_status, cons_department = cursor.fetchall()[0]
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

    # Если консультант уже отправлял пинг дежурному, то повторный пинг не отправляем.
    if dezh_status == 1:
        bot.edit_message_text(
                chat_id=cons_uid,
                message_id=message_id,
                text="А-та-та, ожидай пока ответят на предыдущий пинг.")
        return

    # Пинг со стороны ОО
    elif call.data == "request_dezh_uc":

        ans1_btn = types.InlineKeyboardButton(
            text="Главный.", callback_data="response_dezh_f")
        ans2_btn = types.InlineKeyboardButton(
            text="Временный.", callback_data="response_dezh_h")
        kbrd.row(ans1_btn, ans2_btn)

        super_text = "ИЗ ОТДЕЛА ОБУЧЕНИЯ\nТут дежурного ищет {}. [{},{}]".format(user_info, cons_uid, message_id)

        d_type = 'dezh'
        cons_text = "Дежурный ищется, подожди немного"\
                "\nПримерное время ожидания ответа {} мин.".format(waiting_time)

        console_text = 'Поиск дежурки из ОО'

    # ПИНГ дежурки для обеда
    elif call.data == 'request_dezh_break_time':

        ans_btn = types.InlineKeyboardButton(
                text="Откликнуться.", callback_data="response_dezh_break_time")
        kbrd.row(ans_btn)

        super_text = "{} {}\n'Я хотел пойти в перерыв, но тут такое произшло!', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        d_type = 'break_time'
        cons_text = "Ждем-с ответа..."\
                    "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "{} пропустил свой Want / Very Want.".format(user_info)

    # ПИНГ дежурки для визии
    elif call.data == 'request_dezh_reboot':

        reboot_yes_btn = types.InlineKeyboardButton(
                text="Можно", callback_data="response_dezh_reboot_yes")
        reboot_no_btn = types.InlineKeyboardButton(
                text="Неможно", callback_data="response_dezh_reboot_no")
        kbrd.row(reboot_yes_btn)
        kbrd.row(reboot_no_btn)

        super_text = "{} {}\n'Нужно на супервизию, можно?', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        d_type = 'reboot'
        cons_text = "Узнаю реакцию супервизора..."\
                    "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "{} нужно уйти на супервизию.".format(user_info)

    # ПИНГ дежурки для блица
    elif call.data == 'request_dezh_op_time':

        ans1_btn = types.InlineKeyboardButton(
                text="Согласовать", callback_data="response_dezh_op_time")
        kbrd.row(ans1_btn)

        super_text = "{} {}\n'Мне нужно пройти блиц.', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        d_type = 'op_time'
        cons_text = "Ждем ответа от дежурного. Кнопка для отмены все ещё внизу."\
                    "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "Хочет пройти блиц {}".format(user_info)

    # ПИНГ Дежурного
    elif call.data == 'request_dezh_other':

        ans1_btn = types.InlineKeyboardButton(
                text="Главный", callback_data="response_dezh_f")
        ans2_btn = types.InlineKeyboardButton(
                text="Временный", callback_data="response_dezh_h")
        ans3_btn = types.InlineKeyboardButton(
                text="Ответить", callback_data="response_dezh_f")
        if cons_department == 1 or cons_department == 2:
            kbrd.row(ans1_btn)
            kbrd.row(ans2_btn)
        else:
            kbrd.row(ans3_btn)

        super_text = "{} {}\n'Дежурка, где же ты, родименький?', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        d_type = 'dezh'
        cons_text = "Дежурка уже ищется"\
                    "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "Ищет дежурку {}".format(user_info)

    # Обучение
    elif call.data == 'request_dezh_study':

        ans1_btn = types.InlineKeyboardButton(
                text="Разрешить.", callback_data="response_dezh_study_yes")
        ans2_btn = types.InlineKeyboardButton(
                text="Отказать.", callback_data="response_dezh_study_no")
        kbrd.row(ans1_btn)
        kbrd.row(ans2_btn)

        super_text = "{} {}\n'Не хочу жениться/замуж, хочу учиться!', говорит {}. [{},{}]".format(tag, cons_adress, user_info, cons_uid, message_id)
        d_type = 'study'
        cons_text = "Ждемс-с пока решится твоя судьбинушка."\
                    "\nПримерное время ожидания ответа {} мин.".format(waiting_time)
        console_text = "Учеба/прослушка {}".format(user_info)

    is_today(cons_department)
    update_calls(d_type, cons_department)
    update_dezh_status(cons_uid, message_id, d_type, 1, False)

    bot.send_message(
            chat_id=admin_chat_id,
            text=super_text,
            reply_markup=kbrd)

    bot.edit_message_text(
            chat_id=cons_uid,
            message_id=message_id,
            text=cons_text,
            reply_markup=dezh_cancel_kbrd)

    print_in_console(
            text=console_text,
            date=datetime.datetime.now(), fullname="")
