from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import start, balance, play_spin, play_casino, play_dice, buy, button, help_command, help_text_command
from config import TOKEN

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Установка команд для меню
    updater.bot.set_my_commands([
        ('start', '🎲 Играть'),
        ('help', '📖 Помощь')
    ])

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("spin", play_spin))
    dp.add_handler(CommandHandler("casino", play_casino))
    dp.add_handler(CommandHandler("dice", play_dice, pass_args=True))
    dp.add_handler(CommandHandler("buy", buy, pass_args=True))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("помощь", help_text_command))
    dp.add_handler(CallbackQueryHandler(button))

    # Обработчики команд без символа /
    dp.add_handler(CommandHandler("баланс", balance))
    dp.add_handler(CommandHandler("спин", play_spin))
    dp.add_handler(CommandHandler("казино", play_casino))
    dp.add_handler(CommandHandler("кубик", play_dice, pass_args=True))
    dp.add_handler(CommandHandler("купить", buy, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
