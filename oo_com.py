import sqlite3

from telebot import types

from functions import make_statistic, oo_info
from misc import DB_DIR, OO_DIR


def oo_com(bot, message):

	"""Команды для отдела обучения."""
	if message.text == "Дежурный":
		choice_kbrd = types.InlineKeyboardMarkup()
		uc_dezh_btn = types.InlineKeyboardButton(
				text="Экстерн", callback_data='request_uc_dezh')
		choice_kbrd.row(uc_dezh_btn)
		bot.send_message(
				chat_id=message.from_user.id,
				text='Какого дежурного ищем?',
				reply_markup=choice_kbrd)

	# Отчет по работе стажеров
	elif message.text == "Отчет":
		make_statistic(3)
		filename = REPORTS_DIR+"СТ_{}_{}.xlsx".format(datetime.datetime.now().year, datetime.datetime.now().month)
		with open(filename, 'rb') as report_f:
			bot.send_document(message.from_user.id, report_f)

	oo_info(bot, message)
