import random
from database import get_user, update_balance, update_businesses, get_business_levels

BUSINESSES = {
    "Банк ВТБ": 10000,
    "Сбербанк": 12000,
    "Стройка": 8000,
    "Ферма": 5000,
    "Торговый Центр": 15000
}

UPGRADE_COSTS = {
    "Банк ВТБ": 2000,
    "Сбербанк": 2400,
    "Стройка": 1600,
    "Ферма": 1000,
    "Торговый Центр": 3000
}

def spin(username):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    
    result = random.choice(['Победа', 'Проигрыш'])
    if result == 'Победа':
        update_balance(username, 200)
        return "Вы выиграли 200₽ в игре «Спин»!"
    else:
        update_balance(username, -100)
        return "Вы проиграли 100₽ в игре «Спин». Попробуйте снова!"

def casino(username):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    
    result = random.choice(['Большой выигрыш', 'Малый выигрыш', 'Проигрыш'])
    if result == 'Большой выигрыш':
        update_balance(username, 1000)
        return "Вы выиграли 1000₽ в игре «Казино»!"
    elif result == 'Малый выигрыш':
        update_balance(username, 300)
        return "Вы выиграли 300₽ в игре «Казино»!"
    else:
        update_balance(username, -500)
        return "Вы проиграли 500₽ в игре «Казино». Попробуйте снова!"

def dice(username, guess, bet):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    if user.balance < bet:
        return "У вас недостаточно средств для ставки."
    
    number = random.randint(1, 6)
    if guess == number:
        winnings = bet * 6
        update_balance(username, winnings)
        return f"Вы угадали число {number} и выиграли {winnings}₽ в игре «Кубик»!"
    else:
        update_balance(username, -bet)
        return f"Вы не угадали число {number} и проиграли {bet}₽ в игре «Кубик». Попробуйте снова!"

def buy_business(username, business):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    cost = BUSINESSES.get(business)
    if cost is None:
        return "Такого бизнеса не существует."
    if user.balance >= cost:
        update_balance(username, -cost)
        update_businesses(username, business)
        return f"Вы купили бизнес: {business} за {cost}₽."
    else:
        return "У вас недостаточно средств для покупки этого бизнеса."

def upgrade_business(username, business):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    cost = UPGRADE_COSTS.get(business)
    if cost is None:
        return "Такого бизнеса не существует."
    if user.balance >= cost:
        update_balance(username, -cost)
        update_businesses(username, business, level=1)
        level = get_business_levels(username)[business]
        return f"@{username}, вы успешно улучшили свой бизнес {business} до уровня {level}!"
    else:
        return "У вас недостаточно средств для улучшения этого бизнеса."
