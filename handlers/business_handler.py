from telebot import TeleBot
from business_logic.business_logic import buy_business

def register_business_handler(bot: TeleBot):
    @bot.message_handler(commands=['buy_business'])
    def cmd_buy_business(message):
        buy_business(bot, message)
