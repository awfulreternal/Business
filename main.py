from telegram.ext import Updater
from handlers import start, move, explore, inventory, craft, button

def main():
    # Замените 'YOUR_TOKEN' на ваш токен, полученный от BotFather
    TOKEN = '7013013514:AAG_KcuXDjDBjsRhT65hJE8mzOc9CdpnfCc'
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('move', move))
    dp.add_handler(CommandHandler('explore', explore))
    dp.add_handler(CommandHandler('inventory', inventory))
    dp.add_handler(CommandHandler('craft', craft))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
