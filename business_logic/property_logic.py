from database.db import get_user, create_user, get_properties, purchase_property

def start_game(bot, message):
    user = get_user(message.from_user.id)
    if not user:
        create_user(message.from_user.id)
        bot.send_message(message.chat.id, "Игра началась! Добро пожаловать!")
    else:
        bot.send_message(message.chat.id, "Вы уже начали игру!")

def show_properties(bot, message):
    properties = get_properties()
    response = "Доступные недвижимости:\n"
    for prop in properties:
        response += f"{prop['name']} - ${prop['price']}\n"
    bot.send_message(message.chat.id, response)

def buy_property(bot, message):
    prop_id = int(message.text.split()[1])
    user = get_user(message.from_user.id)
    if user:
        success = purchase_property(user, prop_id)
        if success:
            bot.send_message(message.chat.id, "Недвижимость куплена успешно!")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств!")
    else:
        bot.send_message(message.chat.id, "Вы должны начать игру сначала! Используйте команду /start.")
