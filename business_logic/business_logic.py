def buy_business(bot, message):
    try:
        business_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректный идентификатор бизнеса.")
        return

    user = get_user(message.from_user.id)
    if user:
        success = purchase_business(user, business_id)
        if success:
            bot.send_message(message.chat.id, "Бизнес куплен успешно!")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств или бизнес не существует!")
    else:
        bot.send_message(message.chat.id, "Вы должны начать игру сначала! Используйте команду /start.")
