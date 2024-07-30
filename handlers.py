from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from game_data import init_player, get_player, set_position, get_position, update_inventory, craft_item, world, resources

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    keyboard = [
        [InlineKeyboardButton("Играть", callback_data='start_game')],
        [InlineKeyboardButton("Продолжить", callback_data='continue_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if user_id not in get_player(user_id):
        update.message.reply_text(
            'Добро пожаловать в игру! Нажмите "Играть" для создания нового мира.',
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            'Нажмите "Продолжить" для возобновления игры.',
            reply_markup=reply_markup
        )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    
    if query.data == 'start_game':
        init_player(user_id)
        query.edit_message_text(
            'Игра началась! Вы находитесь в своём мире. Используйте /move <up|down|left|right> для перемещения, /inventory для просмотра инвентаря и /craft <item> для крафта.'
        )
    
    elif query.data == 'continue_game':
        player = get_player(user_id)
        if player:
            position = player['position']
            inventory = player['inventory']
            query.edit_message_text(
                f'Ваше текущее положение: {position}. Ваш инвентарь: {inventory}. Используйте /move <up|down|left|right> для перемещения и /explore для исследования мира.'
            )
        else:
            query.edit_message_text('Вы не начали игру. Нажмите "Играть" для начала новой игры.')

def move(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not get_player(user_id):
        update.message.reply_text('Сначала используйте /start для начала игры.')
        return

    direction = context.args[0] if context.args else None
    if direction not in ['up', 'down', 'left', 'right']:
        update.message.reply_text('Пожалуйста, используйте /move <up|down|left|right> для перемещения.')
        return

    x, y = get_position(user_id)
    if direction == 'up':
        y = min(y + 1, world_size - 1)
    elif direction == 'down':
        y = max(y - 1, 0)
    elif direction == 'left':
        x = max(x - 1, 0)
    elif direction == 'right':
        x = min(x + 1, world_size - 1)

    set_position(user_id, (x, y))
    update.message.reply_text(
        f'Вы переместились на позицию {get_position(user_id)}. Используйте /explore для исследования мира.'
    )

def explore(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not get_player(user_id):
        update.message.reply_text('Сначала используйте /start для начала игры.')
        return

    x, y = get_position(user_id)
    resource = world[y][x]
    if resource in resources:
        update_inventory(user_id, resource)
        update.message.reply_text(
            f'Вы нашли {resources[resource]} {resource}! Ваш инвентарь: {get_player(user_id)["inventory"]}.'
        )
    else:
        update.message.reply_text('Здесь нет ресурсов.')

def inventory(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not get_player(user_id):
        update.message.reply_text('Сначала используйте /start для начала игры.')
        return

    inventory = get_player(user_id)['inventory']
    items = ', '.join(f'{resources[item]} {item}: {quantity}' for item, quantity in inventory.items() if quantity > 0)
    if items:
        update.message.reply_text(f'Ваш инвентарь: {items}')
    else:
        update.message.reply_text('Ваш инвентарь пуст.')

def craft(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not get_player(user_id):
        update.message.reply_text('Сначала используйте /start для начала игры.')
        return

    item = ' '.join(context.args)
    if craft_item(user_id, item):
        update.message.reply_text(f'Вы успешно создали {item}!')
    else:
        update.message.reply_text(f'Не удалось создать {item}. Убедитесь, что у вас есть все необходимые ресурсы и правильное название предмета.')
