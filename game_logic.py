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

BUSINESS_INCOMES = {
    "Банк ВТБ": 500,
    "Сбербанк": 600,
    "Стройка": 400,
    "Ферма": 300,
    "Торговый Центр": 800
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
        return "У вас недостаточно средств для ставки!"
    
    dice_roll = random.randint(1, 6)
    if guess == dice_roll:
        winnings = bet * 6
        update_balance(username, winnings)
        return f"Вы угадали! Кубик выпал на {dice_roll}. Вы выиграли {winnings}₽!"
    else:
        update_balance(username, -bet)
        return f"Не угадали. Кубик выпал на {dice_roll}. Вы проиграли {bet}₽."

def buy_business(username, business):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    if user.balance < BUSINESSES.get(business, 0):
        return "У вас недостаточно средств для покупки этого бизнеса!"
    
    update_balance(username, -BUSINESSES[business])
    businesses = get_business_levels(username)
    businesses[business] = businesses.get(business, 1)
    update_businesses(username, businesses)
    return f"Вы успешно купили бизнес {business}!"

def upgrade_business(username, business):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    businesses = get_business_levels(username)
    level = businesses.get(business, 1)
    if level < 1:
        return "Этот бизнес не существует у вас."
    
    cost = UPGRADE_COSTS.get(business, 0) * level
    if user.balance < cost:
        return "У вас недостаточно средств для улучшения этого бизнеса."
    
    update_balance(username, -cost)
    businesses[business] = level + 1
    update_businesses(username, businesses)
    return f"Вы успешно улучшили свой бизнес до уровня {level + 1}!"

def apply_business_income(username):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    
    businesses = get_business_levels(username)
    total_income = 0
    for business, level in businesses.items():
        income = BUSINESS_INCOMES.get(business, 0)
        total_income += income * level
    
    update_balance(username, total_income)
    return f"Ваши бизнесы принесли вам {total_income}₽!"

def update_balance(username, amount):
    user = get_user(username)
    if not user:
        return "Вы не зарегистрированы!"
    
    new_balance = user.balance + amount
    if new_balance < 0:
        new_balance = 0
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = ? WHERE username = ?', (new_balance, username))
    conn.commit()
    conn.close()
