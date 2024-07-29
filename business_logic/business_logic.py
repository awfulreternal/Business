from database.db import get_user, purchase_business

def buy_business(bot, message):
    business_id = int(message.text.split()[1])
    user = get_user(message.from_user.id)
    if user:
        success = purchase_business(user, business_id)
        if success:
            bot.send_message(message.chat.id, "Бизнес куплен успешно!")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств!")
    else:
        bot.send_message(message.chat.id, "Вы должны начать игру сначала! Используйте команду /start.")
