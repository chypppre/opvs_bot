import os
import sqlite3

# Токен бота
TOKEN = "806413118:AAG1xI4msHZ2RG26UzaN9q3LUI6fzIjwqtY"

DB_DIR = "/home/irc/bot/svetofor.db"
REPORTS_DIR = "/home/irc/bot/reports/"
PICS_DIR = "/home/irc/bot/pics/"
OO_DIR = "/home/irc/bot/oo/"

# ИД чатов,
CHATS_ID = [-1001153489953, #Экстерн,        0
#            -1001352463732, #экспертов ALL,  1
           # -1001153489953, #ОПВС-ЭПС,       2
#            -1001428933815, #ОЛЕГ,           3
#            -1001389171690, #НАСТАВНИКИ      4
#            -1001381826391, #ФМС + Отелька   5
#            -1001221634075, #КБухгалтерия    6
#            -1001231841324] #Эльба           7
]
    
mydb = sqlite3.connect(DB_DIR)

# БЕРЕМ СПИСОК КОНСУЛЬТАНТОВ ПРИ ЗАПУСКЕ БОТА
staff = []
staff_cursor = mydb.cursor()
staff_sql = "SELECT uid FROM staff"
staff_cursor.execute(staff_sql)
st_list = staff_cursor.fetchall()
for row in st_list:
    uid = row[0]
    staff.append(uid)

# БЕРЕМ СПИСОК СУПЕРОВ
supers = []
supers_cursor = mydb.cursor()
supers_sql = 'SELECT uid FROM supers'
supers_cursor.execute(supers_sql)
su_list = supers_cursor.fetchall()
for row in su_list:
    uid = row[0]
    supers.append(uid)

# БЕРЕМ СПИСОК ПОМОГАТОРОВ
helpers = []
helpers_cursor = mydb.cursor()
helpers_sql = 'SELECT uid FROM helpers'
helpers_cursor.execute(helpers_sql)
he_list = helpers_cursor.fetchall()
for row in he_list:
    uid = row[0]
    helpers.append(uid)

# БЕРЕМ СПИСОК ПИПОВ
pips = []
pips_cursor = mydb.cursor()
pips_sql = 'SELECT uid FROM pips'
pips_cursor.execute(pips_sql)
pip_list = pips_cursor.fetchall()
for row in pip_list:
    uid = row[0]
    pips.append(uid)

# БЕРЕМ СПИСОК СТАЖЕРОВ
interns = []
interns_cursor = mydb.cursor()
interns_sql = 'SELECT uid FROM staff WHERE department=3'
interns_cursor.execute(interns_sql)
interns_list = interns_cursor.fetchall()
for row in interns_list:
    uid = row[0]
    interns.append(uid)

# Отдел обучения
oos = []
oos_cursor = mydb.cursor()
oos_sql = 'SELECT uid FROM staff WHERE department=4'
oos_cursor.execute(oos_sql)
oos_list = oos_cursor.fetchall()
for row in oos_list:
    uid = row[0]
    oos.append(uid)
