from telebot import TeleBot
from business_logic import start_game

def register_start_handler(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        start_game(bot, message)
