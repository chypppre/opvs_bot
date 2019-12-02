import datetime
import sqlite3

from telebot import types

from misc import CHATS_ID, DB_DIR
from functions import *

# !-------------------------КОМАНДЫ КОНСУЛЬТАНТА-------------------------------

def cons_com(bot, message):

    # Собираем информацию о пингующем
    uid = message.from_user.id  # Получаем уникальный id

    mydb = sqlite3.connect(DB_DIR)
    cursor = mydb.cursor()
    sql = """SELECT last_name, first_name, adress, department
            FROM staff
            WHERE uid={}""".format(uid)
    cursor.execute(sql)
    last_name, first_name, adress, department = cursor.fetchall()[0]  # Получаем фамилию, имя и рабочий адрес
    full_name = "{} {} (@{})".format(
            last_name,
            first_name,
            message.from_user.username)
    cursor.close()
    mydb.close()

    chat_id_from = uid  # Получаем id чата с ботом куда будем отправлять ответ на Пинг
    text = message.text

    admin_chat_id = get_admin_chat_id("staff", message.from_user.id)  # Получаем id чата, куда направим запрос на Пинг

    keyboard = types.InlineKeyboardMarkup()
    ping_btn = types.InlineKeyboardButton(
        text="Пинг по инцу.", callback_data="request_ping_product")
    knowledge_ping_btn = types.InlineKeyboardButton(
        text="Привязка знания.", callback_data="request_ping_knowledge")
    # exp_btn = types.InlineKeyboardButton(
    #         text="Эксперт", callback_data="request_ping_exp")
    # exp_ud_btn = types.InlineKeyboardButton(
    #         text="УД с экспертом", callback_data="request_ping_exp_ud")

    if department == 1:
        keyboard.row(ping_btn)
        keyboard.row(knowledge_ping_btn)
        # keyboard.row(exp_btn)
        # keyboard.row(exp_ud_btn)
    elif department == 3:
        keyboard.row(ping_btn)
        keyboard.row(knowledge_ping_btn)
        keyboard.row(check_btn)
        keyboard.row(hard_btn)

    # ОТПРАВКА ПИНГА
    # Только для отдела УЦ
    # if department == 1:
        # Пожелания, замечания по работе и ответы супервизоров
    #    if message.chat.id not in CHATS_ID and message.text == "Обратная связь":
    #        keyboard = types.InlineKeyboardMarkup()
    #        wish_btn = types.InlineKeyboardButton(
    #                text="Пожелания",
    #                url="https://staff.skbkontur.ru/survey/5ca9cb67fae04e2d9857a357")
    #        remark_btn = types.InlineKeyboardButton(
    #                text="Замечания",
    #                url="https://staff.skbkontur.ru/survey/5c90936bfae04e168c6c4147")
    #        ans_btn = types.InlineKeyboardButton(
    #                text="Ответы супервизоров",
    #                url="https://wiki.skbkontur.ru/pages/viewpage.action?pageId=269013060")
    #        keyboard.row(wish_btn)
    #        keyboard.row(remark_btn)
    #        keyboard.row(ans_btn)
    #        bot.send_message(
    #                chat_id=chat_id_from,
    #                text='Доработки, недовольства и их решения.',
    #                reply_markup=keyboard)

    # Получение сообщения с типом пингов.
    if message.chat.id not in CHATS_ID and message.text == "Пинг":

            bot.send_message(
                    chat_id=chat_id_from,
                    text='Выбери тип пинга:',
                    reply_markup=keyboard)

    # Поиск дежурного.
    elif message.chat.id not in CHATS_ID and message.text == "Дежурный":

        options_kbrd = types.InlineKeyboardMarkup()
        dezh_btn = types.InlineKeyboardButton(
                text="Прочее.", callback_data="request_dezh_other")
        dezh_norm_btn = types.InlineKeyboardButton(
                text="Дежурный.", callback_data="request_dezh_other")
        break_btn = types.InlineKeyboardButton(
                text="Перерыв.", callback_data="request_dezh_break_time")
        reboot_btn = types.InlineKeyboardButton(
                text="Супервизия.", callback_data="request_dezh_reboot")
        op_btn = types.InlineKeyboardButton(
                text="Блиц-опрос.", callback_data="request_dezh_op_time")
        # miss_btn = types.InlineKeyboardButton(
        #         text="Пропустил фикс.перерыв", callback_data="request_dezh_miss_fix_break")
        study_btn = types.InlineKeyboardButton(
                text="Обучение/Самопрослушка", callback_data="request_dezh_study")
        if department not in [5,6]:
            options_kbrd.row(study_btn)
            options_kbrd.row(break_btn)
            options_kbrd.row(reboot_btn)
            options_kbrd.row(op_btn)
            options_kbrd.row(dezh_btn)
            # options_kbrd.row(miss_btn)
        else:
            options_kbrd.row(dezh_norm_btn)

        # Отправляется сообщение в "Админский чат"
        bot.send_message(
                chat_id=chat_id_from,
                text="Причина запроса:",
                reply_markup=options_kbrd)

    # ПРОЧИЕ
    elif message.chat.id not in CHATS_ID and message.text == "Прочие":
        keyboard = types.InlineKeyboardMarkup()
        meme_btn = types.InlineKeyboardButton(
                text="ASCII Memes",
                callback_data="memes")
        home_btn = types.InlineKeyboardButton(
                text="Домашняя",
                url="https://wiki.skbkontur.ru/pages/viewpage.action?pageId=226850279")
        test_btn = types.InlineKeyboardButton(
                text="Тест",
                callback_data="test")
 #       about_btn = types.InlineKeyboardButton(
 #               text="About",
 #               callback_data="about")
        keyboard.row(meme_btn)
        keyboard.row(home_btn)
        keyboard.row(test_btn)
 #       keyboard.row(about_btn)
        bot.send_message(
                chat_id=chat_id_from,
                text='Прочие команды:',
                reply_markup=keyboard)
