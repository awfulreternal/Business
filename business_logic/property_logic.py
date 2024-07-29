def buy_property(bot, message):
    try:
        prop_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректный идентификатор недвижимости.")
        return

    user = get_user(message.from_user.id)
    if user:
        success = purchase_property(user, prop_id)
        if success:
            bot.send_message(message.chat.id, "Недвижимость куплена успешно!")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств или недвижимость не существует!")
    else:
        bot.send_message(message.chat.id, "Вы должны начать игру сначала! Используйте команду /start.")
