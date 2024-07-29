import telebot
from config import TOKEN
from handlers import register_handlers

bot = telebot.TeleBot(TOKEN)

register_handlers(bot)

if __name__ == '__main__':
    bot.polling(none_stop=True)
