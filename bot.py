import threading

import telebot

from cons_com import cons_com
from etc_com import etc_com
from misc import *
from functions import *
from fix_break import bot_checking
from intern_com import intern_com
from oo_com import oo_com
from pings import callback_com
from pings.cancels import cancel
from pings.request import request_ping, request_dezh
from pings.response import response_ping, response_dezh
from pip_com import pip_com
from supervisors_commands import add_user, delete_user, delete, decline, find_cons


def main(bot):

    @bot.message_handler(commands=['start'])
    def send_start(message):
        """Отправка клавиатуры пользователю по команде /start ."""
        if auth(bot, message.from_user.id):
            department = get_department('staff', message.from_user.id)
            kbrd = create_keyboard(department)

            bot.send_message(
                    chat_id=message.from_user.id,
                    text="Работа, работа, уйди на Федота. (c)",
                    reply_markup=kbrd)

    @bot.message_handler(commands=['addmeplease'])
    def add_boyya(message):
        """Добавление пользователя в БД бота"""
        bot.send_message(
                chat_id=message.from_user.id,
                text="Чтобы нам легче было понять кто ты, пожалуйста, "\
                        "укажи свои фамилию и имя и из какого ты отдела "\
                        "в формате 'Фамилия:Большой Имя:Лебовски 1':"\
                        "\n1 - Отдел Экстерн 1 ВРН")
#                       "\n3 - Стажёр Экстерн 1 ВРН"\)

    @bot.message_handler(commands=['delete'])
    def delete_boyya(message):
        """"Добавление пользователя в БД бота"""
        if is_super(message.from_user.id):
            kbrd = types.InlineKeyboardMarkup()
            cons_btn = types.InlineKeyboardButton(text="Консультанты", callback_data="delete_cons")
            helper_btn = types.InlineKeyboardButton(text="Помогаторы/Наставники", callback_data="delete_helper")
            super_btn = types.InlineKeyboardButton(text="Супервизоры", callback_data="delete_super")
            oo_btn = types.InlineKeyboardButton(text="ОО", callback_data="delete_oo")
            pip_btn = types.InlineKeyboardButton(text="ПиП", callback_data="delete_pip")
            kbrd.row(cons_btn)
            kbrd.row(helper_btn)
            kbrd.row(super_btn)
            kbrd.row(oo_btn, pip_btn)
            text_for_admins = "Кого будем удалять?"
            bot.send_message(
                chat_id=message.from_user.id,
                text=text_for_admins,
                reply_markup=kbrd)

    @bot.message_handler(commands=['help', 'info'])
    def send_help(message):
        if auth(bot, message.from_user.id):
            mydb = sqlite3.connect(DB_DIR)
            cursor = mydb.cursor()
            sql = "SELECT department FROM staff WHERE uid={}".format(message.from_user.id)
            cursor.execute(sql)
            department = cursor.fetchall()[0][0]
            uid = message.from_user.id

            """Отправка ознакомительного текта по команде /help ."""
            help_text = 'Сейчас для бота доступны команды:'\
                        '\n"/start" - общая команда старт.'\
                        '\n"/help" - вызов этого сообщения.'\
                        '\n"/grafik" - для просмотра фиксированного перерыва.'\
                        '\n"/userID" - чтобы узнать свой uid.'\
                        '\n"/chatID" - чтобы узнать uid чата.'\
                        '\n"/addmeplease" - чтобы добавиться в бота.'\
                        '\n"/list" - команда для просмотра списка групп в боте.'\
                        '\n"установить адрес ххх" - прописать свой рабочий адрес в боте.'
            if department == 1:
                help_text += '\n"Пинг" - для поиска свободного визора.'\
                        '\n"Дежурка" - для поиска дежурки.'\
                        '\n"мем" - затригерить бота на ASCII-мемасик.'
            elif department == 3:
                help_text += '\n"Пинг" - для поиска свободного визора.'\
                        '\n"Дежурка" - для поиска дежурки.'
            bot.send_message(chat_id=message.chat.id, text=help_text)
            if is_super(uid):
                admin_text = '-----------------------'\
                        '\n"/report и /report2" - команда для получения отчета по пингам в Excel.'\
                        '\n"установить супервизорский адрес ххх" - прописать рабочий адрес супервизора.'\
                        '\nМожно отправлять сообщения:'\
                        '\nличное uid "текст"'\
                        '\nгрупповое экстерн|суперы|стажеры|помогаторы "текст"'\
                        '\nмассовое "текст"'
                bot.send_message(chat_id=message.from_user.id, text=admin_text)
            if is_helper(uid):
                helper_text = '-----------------------'\
                        '\n"установить помогаторский адрес xxx" - установить рабочий адрес в качестве помогатора'
                bot.send_message(chat_id=message.from_user.id, text=helper_text)
            if is_pip(uid) or is_mentor(uid):
                pip_text =  '-----------------------'\
                        '\n"визия *ФИ*" - текстовая команда для вызова консультанта на визию.'\
                        '\n"пз *ФИ*" - текстовая команда для вызова консультанта на проверку знаний.'
                bot.send_message(chat_id=message.from_user.id, text=pip_text)

    # @bot.message_handler(commands=['grafik'])
    # def send_grafik(message):
    #     """Посмотреть график"""
    #     bot_checking.send_grafik(bot, message.from_user.id)

    @bot.message_handler(commands=['chatID'])
    def send_chatID(message):
        """Отправка ID чата в суперский чат ."""
        bot.send_message(
                chat_id=CHATS_ID[0],
                text="{} - {}".format(message.chat.title, message.chat.id))

    @bot.message_handler(commands=['userID'])
    def send_userID(message):
        """Отправка ID чата в суперский чат ."""
        bot.send_message(
                chat_id=message.from_user.id,
                text="{} - {}".format(message.from_user.username, message.from_user.id))

    @bot.message_handler(commands=['focus'])
    def send_focus(message):
        """ФОКУС ПОКУС ЕПТА."""
        kbrd = types.InlineKeyboardMarkup()
        focus_btn = types.InlineKeyboardButton(text='Гля сюды', url="qwic://incident/19854786")
        kbrd.row(focus_btn)
        bot.send_message(
                chat_id=message.from_user.id,
                text="ЕМАЁ МАМАЯ МИЯ",
                reply_markup=kbrd)

    @bot.message_handler(commands=['list'])
    def send_cons_list(message):
        """Отправка списка консультантов."""
        if auth(bot, message.from_user.id):
            lists = types.InlineKeyboardMarkup()
            cons_btn = types.InlineKeyboardButton(text='Консультанты КЭ', callback_data="cons")
            helper_btn = types.InlineKeyboardButton(text='Помогаторы', callback_data="helpers")
            pip_btn = types.InlineKeyboardButton(text='ПиПы', callback_data="pips")
            oo_btn = types.InlineKeyboardButton(text='ОО', callback_data="oos")
            super_btn = types.InlineKeyboardButton(text='Супервизоры', callback_data="supers")
            intern_btn = types.InlineKeyboardButton(text='Стажеры', callback_data="interns")
            lists.add(cons_btn, helper_btn, super_btn)
            lists.add(pip_btn, oo_btn, intern_btn)
            bot.send_message(
                    chat_id=message.from_user.id,
                    text='Выбирай.',
                    reply_markup=lists)

    @bot.message_handler(commands=['report'])
    def report(message):
        """Формирование простого отчета"""
        if is_super(message.from_user.id) and message.chat.id not in CHATS_ID:

            department = get_department("supers", message.from_user.id)

            if department == 1:
                make_statistic(1)
                filename = REPORTS_DIR+"КЭ_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
            elif department == 2:
                make_statistic(2)
                filename = REPORTS_DIR+"ФМС_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
            elif department == 5:
                make_statistic(5)
                filename = REPORTS_DIR+"КБ_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
            elif department == 6:
                make_statistic(6)
                filename = REPORTS_DIR+"ЭЛЬБА_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
            with open(filename, 'rb') as report_f:
                bot.send_document(
                        message.from_user.id,
                        report_f)

    @bot.message_handler(commands=['report2'])
    def report(message):
        """Формирование простого отчета"""
        if is_super(message.from_user.id) or is_helper(message.from_user.id) or is_oo(message.from_user.id) \
                and (message.chat.id not in CHATS_ID):
            make_statistic(3)
            filename = REPORTS_DIR+"СТ_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
            with open(filename, 'rb') as report_f:
                bot.send_document(
                        message.from_user.id,
                        report_f)

    # Создание логики:
    @bot.message_handler(content_types=["text"])
    def any_msg(message):
        """Реализация головы бота."""

        uid = message.from_user.id
        chat_id_from = message.chat.id

        if chat_id_from not in CHATS_ID:

            if message.text.startswith("Фамилия:"):
                text = message.text
                text = text.split(" ")
                last_name = text[0].split(":")[1]
                first_name = text[1].split(":")[1]
                department = text[2]
                add_user.add_to_tempo(uid, last_name, first_name, department)
                bot.send_message(
                        chat_id=message.from_user.id,
                        text="Отправил запрос на добавление тебя к боту. Жди ответ...")
                add_user.send_add_request(bot, uid)
                return 0

            if auth(bot, uid):
                department = get_department("staff", uid)

                if message.text.lower().startswith('установить'):
                    status(bot, message.text, message.from_user.id)
                elif message.text.lower().startswith('найти'):
                    find_cons.find_cons_logic(bot, message)
                # ДЛЯ ОТПРАВКИ СООБЩЕНИЙ ЧЕРЕЗ БОТА
                if is_super(uid):
                    # ВСЕ
                    try:
                        if message.text.lower().startswith('массовое'):
                            mass_message(bot, message.text, message.from_user.id)
                        # ОПРЕДЕЛЕННОЙ ГРУППЕ
                        elif message.text.lower().startswith('групповое'):
                            group_message(bot, message.text, message.from_user.id)
                        # КОМУ-ТО ЛИЧНО
                        elif message.text.lower().startswith('личное'):
                            private_message(bot, message.text, message.from_user.id)
                    except Exception as e:
                        bot.send_message(
                                chat_id=message.from_user.id,
                                text="Произошла ошибка.\n{}".format(e))

                # Для основных конусльтантов
                if not is_intern(uid):
                    try:
                        etc_com(bot, message)  # Разные команды
                        cons_com(bot, message)  # Консультант
                        pip_com(bot, message)  # Проверка и Прослушка
                        # super_com(bot, message)  # Супервизорская
                    except Exception as e:
                        bot.send_message(
                                chat_id=CHATS_ID[0],
                                text="{} убил бота. Ошибка {}".format(
                                        str(message.from_user.username), str(e)))
                # Для О
                if is_oo(uid):
                    try:
                        oo_com(bot, message)
                    except Exception as e:
                        print("ОШИБКА в ОО\n"+str(e))
                # Для стажеров
                if is_intern(uid):
                    try:
                        intern_com(bot, message)
                        etc_com(bot, message)
                    except Exception as e:
                        print("ОШИБКА в intern\n"+str(e))


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):

        """Обработка колл-бэков."""
        if is_super(call.from_user.id): # Только для супервизоров
            if call.data.startswith("delete"):
                delete_user.delete_user(bot, call)
                delete.delete(bot, call)
            elif call.data.startswith("add"):
                add_user.add_user(bot, call)
            elif call.data == "decline":
                decline.decline_logic(bot, call, uid)
        if is_super(call.from_user.id) or is_helper(call.from_user.id) or is_mentor(call.from_user.id): # Для отвечающих на пинги
            if call.data.startswith("response_dezh"):
                response_dezh.response_dezh(bot, call)
            elif call.data.startswith("response_ping"):
                response_ping.response_ping(bot, call)
        if auth(bot, call.from_user.id):    # Для всех
            if call.data.startswith("request_dezh"):
                request_dezh.request_dezh(bot, call)
            elif call.data.startswith("request_ping"):
                request_ping.request_ping(bot, call)
            callback_com.other_callbacks(bot, call)
            cancel.cancel_logic(bot, call)

    print("\n!!!!Бот завелся!!!!\n")
    bot.send_message(203652496, 'Готов вкалывать. (с)')
    bot.polling(none_stop=True)


if __name__ == "__main__":
    while True:
        try:
            # Создание самого бота
            bot = telebot.TeleBot(TOKEN)
            # my_thread = threading.Thread(target=bot_checking.auto_alert, args=(bot,))
            # my_thread.start()
            main(bot)
        except:
            bot.send_message(
                chat_id=203652496,
                text="Пагип, умир!!!")
            del bot
