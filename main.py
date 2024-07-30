import telebot
from config import TOKEN
from game import Game
from messages import MESSAGES

bot = telebot.TeleBot(TOKEN)
game = Game()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, MESSAGES['welcome'])

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, MESSAGES['help'])

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    city_info = game.get_city_info(user_id)
    bot.send_photo(message.chat.id, city_info['image'])
    bot.reply_to(message, city_info['status'])

@bot.message_handler(commands=['create'])
def create_civilization(message):
    user_id = message.from_user.id
    success, msg = game.create_civilization(user_id)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['upgrade'])
def upgrade_building(message):
    user_id = message.from_user.id
    params = message.text.split(maxsplit=1)
    if len(params) > 1:
        building = params[1]
        success, msg = game.upgrade_building(user_id, building)
    else:
        msg = MESSAGES['missing_params']
    bot.reply_to(message, msg)

@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    params = message.text.split(maxsplit=1)
    if len(params) > 1:
        target_civilization = params[1]
        success, msg = game.attack_city(user_id, target_civilization)
    else:
        msg = MESSAGES['missing_params']
    bot.reply_to(message, msg)

@bot.message_handler(commands=['quest'])
def complete_quest(message):
    user_id = message.from_user.id
    params = message.text.split(maxsplit=1)
    if len(params) > 1:
        quest_type = params[1]
        success, msg = game.complete_quest(user_id, quest_type)
    else:
        msg = MESSAGES['missing_params']
    bot.reply_to(message, msg)

@bot.message_handler(commands=['donate'])
def donate(message):
    user_id = message.from_user.id
    params = message.text.split(maxsplit=1)
    if len(params) > 1:
        try:
            donate_amount = int(params[1])
            success, msg = game.donate(user_id, donate_amount)
        except ValueError:
            msg = MESSAGES['invalid_amount']
    else:
        msg = MESSAGES['missing_params']
    bot.reply_to(message, msg)

if __name__ == '__main__':
    bot.polling()
