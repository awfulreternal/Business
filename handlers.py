from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import create_user, get_user, get_business_levels
from game_logic import spin, casino, dice, buy_business, upgrade_business

def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    if not get_user(username):
        create_user(username)
    update.message.reply_text(
        "🎮 Добро пожаловать в GameMaster! 🎮\n\n"
        "Вы успешно зарегистрированы! 🎉\n"
        "Здесь вы можете играть в игры, покупать бизнесы и зарабатывать рубли. 💸\n"
        "Используйте команды для взаимодействия с ботом и наслаждайтесь игрой! 🚀"
    )

def balance(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    user = get_user(username)
    if user:
        update.message.reply_text(f"Ваш баланс: {user.balance}₽")
    else:
        update.message.reply_text("Вы не зарегистрированы!")

def play_spin(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    result = spin(username)
    update.message.reply_text(result)

def play_casino(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    result = casino(username)
    update.message.reply_text(result)

def play_dice(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    args = context.args
    if len(args) != 2:
        update.message.reply_text("Использование: кубик [число от 1 до 6] [ставка]")
        return
    guess = int(args[0])
    if guess < 1 or guess > 6:
        update.message.reply_text("Число должно быть от 1 до 6.")
        return
    try:
        bet = float(args[1])
    except ValueError:
        update.message.reply_text("Ставка должна быть числом.")
        return
    result = dice(username, guess, bet)
    update.message.reply_text(result)

def buy(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    args = context.args
    if len(args) != 1:
        update.message.reply_text("Использование: купить [бизнес]")
        return
    business = args[0]
    result = buy_business(username, business)
    update.message.reply_text(result)
    if "купили бизнес" in result:
        businesses = get_business_levels(username)
        level = businesses.get(business, 1)
        keyboard = [
            [InlineKeyboardButton(f"Улучшить {business} (Уровень {level})", callback_data=f"upgrade_{business}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"{business} уровень {level}", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    username = query.from_user.username
    query.answer()
    
    if query.data.startswith("upgrade_"):
        business = query.data.split("_")[1]
        result = upgrade_business(username, business)
        query.edit_message_text(text=result)
        businesses = get_business_levels(username)
        level = businesses.get(business, 1)
        keyboard = [
            [InlineKeyboardButton(f"Улучшить {business} (Уровень {level})", callback_data=f"upgrade_{business}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(f"{business} уровень {level}", reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "📖 Помощь по командам 📖\n\n"
        "🎲 /start - Начать взаимодействие с ботом.\n"
        "💰 /balance - Проверка своего баланса.\n"
        "🏢 /buy бизнес (название бизнеса) - Купить бизнес.\n"
        "🎰 /casino (сумма/все) - Играть в казино.\n"
        "🎡 /spin (все/сумма) - Играть в игру «Спин».\n"
        "🎲 /dice (число от 1 до 6)-(ставка все/сумма) - Играть в игру «Кубик».\n"
    )
    update.message.reply_text(help_text)

def help_text_command(update: Update, context: CallbackContext):
    help_text = (
        "📖 Помощь по командам 📖\n\n"
        "🎲 Начать - Начать взаимодействие с ботом.\n"
        "💰 Баланс - Проверка своего баланса.\n"
        "🏢 Купить бизнес [название бизнеса] - Купить бизнес.\n"
        "🎰 Казино (сумма/все) - Играть в казино.\n"
        "🎡 Спин (все/сумма) - Играть в игру «Спин».\n"
        "🎲 Кубик (число от 1 до 6)-(ставка все/сумма) - Играть в игру «Кубик».\n"
    )
    update.message.reply_text(help_text)
