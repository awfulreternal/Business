import random

# Игровые данные
world_size = 20  # Размер мира (20x20)
resources = {'wood': '🌳', 'stone': '🪨', 'iron': '⛏️'}
world = [[random.choice(list(resources.keys())) for _ in range(world_size)] for _ in range(world_size)]

# Игроки и их данные
players = {}

def init_player(user_id):
    if user_id not in players:
        players[user_id] = {
            'position': (0, 0),
            'inventory': {'wood': 5, 'stone': 5, 'iron': 1},
            'crafted_items': []
        }

def get_player(user_id):
    return players.get(user_id, None)

def set_position(user_id, position):
    if user_id in players:
        players[user_id]['position'] = position

def get_position(user_id):
    return players.get(user_id, {}).get('position', (0, 0))

def update_inventory(user_id, resource):
    if user_id in players and resource in players[user_id]['inventory']:
        players[user_id]['inventory'][resource] += 1
        x, y = players[user_id]['position']
        world[y][x] = random.choice(list(resources.keys()))

def craft_item(user_id, item):
    recipes = {
        'axe': {'wood': 5, 'stone': 2},
        'pickaxe': {'wood': 3, 'iron': 2}
    }
    if item in recipes:
        required = recipes[item]
        player_inventory = players[user_id]['inventory']
        if all(player_inventory.get(res, 0) >= qty for res, qty in required.items()):
            for res, qty in required.items():
                player_inventory[res] -= qty
            players[user_id]['crafted_items'].append(item)
            return True
    return False
