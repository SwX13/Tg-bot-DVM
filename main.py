import os
from datetime import timedelta
from datetime import datetime
import telebot

import sqlite3
from telebot import types
from dadata import Dadata

DADATA_KEY = os.environ["Dadata_API_Token"]
TELEGRAM_TOKEN = os.environ["DVM_BOT"]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
dadata = Dadata(DADATA_KEY)
# с подпиской
btn_Check_Compapy = types.InlineKeyboardButton("📋 Проверить организацию по ИНН", callback_data="inn")
btn_Calc_Smeta = types.InlineKeyboardButton("🧮 Расчет сметы", callback_data="smeta")
btn_nalg_con = types.InlineKeyboardButton("💼 Налоговый консалтинг", callback_data="nalcon")
btn_dolj_osm = types.InlineKeyboardButton("🛡️ Должная осмотрительность", callback_data="dolosm")

# без подписки
btn_What_Check_inn = types.InlineKeyboardButton("❓ Зачем проверять контр-агентов?", callback_data="whatinn")
btn_What_Smeta = types.InlineKeyboardButton("❓ Зачем производить расчет сметы?", callback_data="whatsmeta")

btn_tech_support = types.InlineKeyboardButton("🔧 It сопровождение", callback_data="techsupport")

# главное меню
btn_main_menu = types.KeyboardButton("🏠 Главное меню")
btn_Get_Subscribe = types.KeyboardButton("💳 Оформить подписку")

markup_clear = types.InlineKeyboardMarkup()
markup_clear.row(btn_What_Check_inn)
markup_clear.row(btn_What_Smeta)
markup_clear.row(btn_tech_support)

markup_subscribe = types.InlineKeyboardMarkup()
markup_subscribe.row(btn_What_Check_inn)
markup_subscribe.row(btn_What_Smeta)
markup_subscribe.row(btn_nalg_con)
markup_subscribe.row(btn_dolj_osm)
markup_subscribe.row(btn_Check_Compapy)
markup_subscribe.row(btn_Calc_Smeta)
markup_subscribe.row(btn_tech_support)

markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_main_menu.add(btn_main_menu, btn_Get_Subscribe)


@bot.message_handler(commands=['start'])
def start(message):
    create_database()

    bot.send_message(message.chat.id, "Приветствую!", reply_markup=markup_main_menu)
    print_select_options(message)


@bot.message_handler(content_types=["text"])
def check_text(message):
    if message.text.lower().strip() == "🏠 главное меню":
        print_select_options(message)
    elif message.text.lower().strip() == "id":
        bot.send_message(message.chat.id, f"{message.from_user.id}")
    elif message.text.lower().strip() == "💳 оформить подписку":
        subscribe(message)


@bot.callback_query_handler(func=lambda callback: True)
def check_commands(callback):
    if callback.data == "whatinn":
        bot.send_message(callback.message.chat.id, "❗️<u>Почему важно проверять контрагентов?</u>❗️\n\n"
                                                   "1️⃣ <b>Безопасность бизнеса</b>\n"
                                                   "Банки и Центральный Банк РФ тщательно анализируют деятельность компаний. Если ваш контрагент "
                                                   "вызывает сомнения у регуляторов, это может привести к дополнительным проверкам и блокировкам операций.\n\n"
    
                                                   "2️⃣ <b>Снижение бюрократической нагрузки</b>\n"
                                                   "Проверенные контрагенты уменьшают количество запросов от банка, экономя ваше время и ресурсы на сбор документов.\n\n"
    
                                                   "3️⃣ <b>Защита от репутационных и финансовых рисков</b>\n"
                                                   "Работа с ненадёжными партнёрами может привести к включению вашей компании в «чёрные списки» по 115-ФЗ, что грозит:\n"
                                                   "\t- Блокировкой счетов\n"
                                                   "\t- Отказом в обслуживании банками\n"
                                                   "\t- Проблемами с налоговой\n\n"
    
                                                   "4️⃣ <b>Предотвращение мошенничества</b>\n"
                                                   "Проверка контрагентов помогает выявить фирмы-однодневки, компании с признаками нелегальной деятельности или финансовой нестабильности.)",
                         parse_mode="html")

    elif callback.data == "whatsmeta":
        bot.send_message(callback.message.chat.id, """❗️<u>Зачем производить расчет сметы?</u> ❗️
        
1️⃣ <b>Финансовая стабильность</b>
Точный расчет сметы позволяет избежать перерасходов и потерей бюджета. Это важно для поддержания финансовой устойчивости проекта и компании в целом.

2️⃣ <b>Эффективное планирование</b>
Смета помогает четко определить объемы работ и материалы, что снижает количество неожиданных задержек и позволяет оптимально распределить ресурсы.

3️⃣ <b>Защита от рисков</b>
Работа без четкой сметы может привести к финансовым потерям и репутационным рискам. При наличии сметы вы сможете избежать конфликтов с заказчиками и подрядчиками.

4️⃣ <b>Привлечение инвестиций</b>
Правильно оформленная смета способствует укреплению доверия со стороны инвесторов и банков, что важно для получения финансирования и успешной реализации проектов.""",
         parse_mode="html")

    elif callback.data == "techsupport":
        text = "Вы связались с техподдержкой:"
        with open("./resources/techsupport.jpg", "rb") as photo:
            bot.send_photo(callback.message.chat.id, photo, caption=text)

    elif callback.data == "inn":
        text = "🔍 Введите ИНН организации для проверки:"
        with open("./resources/buisness1.png", "rb") as photo:
            bot.send_photo(callback.message.chat.id, photo, caption=text)
            bot.register_next_step_handler(callback.message, check_by_inn)

    elif callback.data == "smeta":
        text = "Нажата расчет сметы:"
        with open("./resources/blueprint.jpg", "rb") as photo:
            bot.send_photo(callback.message.chat.id, photo, caption=text)

    elif callback.data == "nalcon":
        bot.send_message(callback.message.chat.id, "Налоговый консалтинг")

    elif callback.data == "dolosm":
        bot.send_message(callback.message.chat.id, "Должная осмотрительность")


def print_select_options(message):
    con = sqlite3.connect("UsersDB.sqlite")
    cur = con.cursor()

    # check_subscribe_period(message)

    cur.execute("Select * from users where id = %i" % message.from_user.id)
    users = cur.fetchall()

    if len(users) > 0:
        for user in users:
            subscribe = user[1]
            datetime_purcahaise = datetime.fromtimestamp(user[2])
            end_datetime = datetime_purcahaise + timedelta(30)

            print(
                f"user id: {user[0]}\t subscribe: {user[1]}\t purchaise date: {datetime_purcahaise}\t end date: {end_datetime.timestamp()}")
            if subscribe == True and datetime_purcahaise < end_datetime:
                send_message(message, markup_subscribe)
                # bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup_subscribe)
            else:
                send_message(message, markup_clear)
                # bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup_clear)
    else:
        send_message(message, markup_clear)
        # bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup_clear)

    cur.close()
    con.close()


def send_message(message, reply_markup):
    text = "Выберите опцию:"
    with open("./resources/options.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=reply_markup)

def check_subscribe_period(message):
    with sqlite3.connect("UsersDB.sqlite") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
        users = cur.fetchall()

        if len(users) > 0:
            for user in users:
                if datetime.fromtimestamp(user[2]) < datetime.fromtimestamp(user[2]) + timedelta(30):
                    cur.execute("Update users set subscribe = ? where id =?", (False, message.from_user.id))
                    bot.send_message(message.chat.id, f"У вас закончилась подписка. Пожалуйста оформите ее снова для продолжения использования бота")

def subscribe(message):
    with sqlite3.connect("UsersDB.sqlite") as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
        users = cur.fetchall()

        if len(users) > 0:
            for user in users:
                if user[1] == True:
                    bot.send_message(message.chat.id,
                                     f"✅ Вы уже подписаны!\nПодписка активна до {datetime.fromtimestamp(user[2]) + timedelta(30)}")
                    print(f"User: {message.from_user.id} УЖЕ ПОДПИСАН")
                else:
                    cur.execute("Update users set subscribe = ? where id =?", (True, message.from_user.id))
                    bot.send_message(message.chat.id,
                                     f"🔔 Вы успешно возобновили подписку на 1 месяц!\nПодписка активна до {datetime.fromtimestamp(user[2]) + timedelta(30)}")
                    print(f"User: {message.from_user.id} возобновил подписку")
        else:
            cur.execute("Insert into users(id, subscribe,subscribeData) values(?,?,?)",
                        (message.from_user.id, True, datetime.now().timestamp()))
            bot.send_message(message.chat.id, "🎉 Вы успешно оформили подписку на 1 месяц!")
            print(f"User: {message.from_user.id} купил подписку")


def check_by_inn(message):
    print(f"User id: {message.from_user.id}\nUser query: {message.text}")
    inn = message.text.strip()
    if inn.isupper() or inn.islower() or " " in inn:
        bot.send_message(message.chat.id, f"❌ Некорректный ввод ❌")

    else:
        try:
            # Поиск компании по ИНН через Dadata
            result = dadata.find_by_id("party", query=inn)
            if not result:
                bot.reply_to(message, "❌ Организация не найдена.")
                return

            company = result[0]
            name = company["value"]
            ogrn = company["data"]["ogrn"]
            status = company["data"]["state"]["status"]

            # Проверка на массового учредителя (признак риска)
            risk = "⚠️ Риски: есть" if "массовый" in str(company["data"]).lower() else "✅ Риски не обнаружены"

            reply = (
                f"🔍 *{name}*\n"
                f"• ИНН: `{inn}`\n"
                f"• ОГРН: `{ogrn}`\n"
                f"• Статус: `{status}`\n"
                f"• {risk}"
            )
            bot.send_message(message.chat.id, reply, parse_mode="Markdown")

        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    print(f"{message.text.strip()}{inn.isupper()} {inn.islower()} {" " in inn}")


def create_database():
    con = sqlite3.connect("UsersDB.sqlite")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(id int primary key, subscribe boolean, subscribeData timestamp)")
    cur.execute("PRAGMA journal_mode=WAL")
    con.commit()
    cur.close()
    con.close()


bot.polling(none_stop=True)
