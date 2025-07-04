# Before start
**1. Install requirements packages**

**2. Use your tokens:**
- DADATA_KEY
- TELEGRAM_TOKEN

DADATA_KEY = os.environ["Dadata_API_Token"]
TELEGRAM_TOKEN = os.environ["DVM_BOT"]

This project use Environment Variables.

# About bot func
1. <font color="lime"><i>check_subscription_period</i></font> - This method check, if user have or not subscribe. It`s **returnable** func return False if user subscription is out and True another
2. <font color="lime"><i>print_select_options</i></font> - send user options menu by user state (new user, subscriber, )
3. <font color="lime"><i>send_message</i></font> - send message with photo.
4. <font color="lime"><i>subscription</i></font> - subscribe users. Check their in DB, and add new to DB.
5. <font color="lime"><i>create_database</i></font> - create DB if not exist on bot start.
6. <font color="lime"><i>check_text</i></font> - check KeyboardButton events.
7. <font color="lime"><i>check_by_inn</i></font> - get users unput and check. If it doesn`t contains LETTERS and SPACES. Send request to Dadata.
# Main func edit
```python
    # main func 
    def check_commands(callback):
    # delete options message
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    # if user click on "💳 Оформить подписку"
    if callback.data == "getsubscription":
        subscription(callback.from_user.id, callback.message.chat.id)
        
    # if click on "❓ Зачем проверять контр-агентов?"
    elif callback.data == "whatinn":
        ...
    # if click on "❓ Зачем производить расчет сметы?"
    elif callback.data == "whatsmeta":
        ...
    # if click on "🔧 It сопровождение"
    # tamplate
    elif callback.data == "techsupport":
        ...
    
    # check if user have subscription
    elif check_subscription_period(callback.from_user.id, callback.message.chat.id):
        # if click on "📋 Проверить организацию по ИНН"
        # have already working func
        if callback.data == "inn":
            ...
        # if click on "🧮 Расчет сметы"
        # tamplate
        elif callback.data == "smeta":
            ...
        # if click on "💼 Налоговый консалтинг"
        # tamplate
        elif callback.data == "nalcon":
            ...
        # if click on "🛡️ Должная осмотрительность"
        # tamplate
        elif callback.data == "dolosm":
            ...
```
Change bot func in this strings.
# About subscription
- **if user IS NOT in DB** -> add user and print "🎉 Вы успешно оформили подписку на 1 месяц!"
- **if user IS IN DB** ->:
  1. **if user have subscription and period ISN`T OUT** -> print <br>"✅ Вы уже подписаны!\nПодписка активна до {purchase_data + 30 days}"
   2. **if user subscription period IS OUT and user BUY it** -> print <br>"🔔 Вы успешно возобновили подписку на 1 месяц!\nПодписка активна до {purchase_data + 30 days}")
   3. **if user subscription period IS OUT and user DOESN`T BUY it** -> all bot <u>func is locked</u> and print with button <br><u>message</u>:"💔 У вас закончилась подписка.\n😢 Пожалуйста, оформите её снова для продолжения использования бота!"<br><u>button</u>:"💳 Оформить подписку"


