from telebot import TeleBot
from business_logic.property_logic import show_properties, buy_property

def register_property_handler(bot: TeleBot):
    @bot.message_handler(commands=['properties'])
    def cmd_properties(message):
        show_properties(bot, message)

    @bot.message_handler(commands=['buy_property'])
    def cmd_buy_property(message):
        # Проверка, чтобы команда была вызвана с параметрами
        command = message.text.split()
        if len(command) > 1:
            buy_property(bot, message)
        else:
            bot.send_message(message.chat.id, "Использование: /buy_property <id>")
