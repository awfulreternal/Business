from cities import CITY_IMAGES
from messages import MESSAGES
import random

class Game:
    def __init__(self):
        self.civilizations = {}
        self.quests = {
            'explore': 100,
            'build': 200,
            'battle': 300
        }

    def create_civilization(self, user_id):
        if user_id in self.civilizations:
            return False, MESSAGES['already_exists']
        self.civilizations[user_id] = {
            'city': 'small_town',
            'level': 1,
            'gold': 500,
            'gems': 0,
            'buildings': {'barracks': 1, 'farm': 1},
            'troops': 100,
            'quests_completed': 0
        }
        return True, MESSAGES['created']

    def get_city_info(self, user_id):
        if user_id not in self.civilizations:
            return {'status': MESSAGES['no_civilization'], 'image': CITY_IMAGES['default']}
        civ = self.civilizations[user_id]
        city = civ['city']
        level = civ['level']
        return {
            'status': MESSAGES['status'].format(
                city=city,
                level=level,
                gold=civ['gold'],
                gems=civ['gems'],
                troops=civ['troops'],
                buildings=civ['buildings']
            ),
            'image': CITY_IMAGES.get(city, CITY_IMAGES['default'])
        }

    def upgrade_building(self, user_id, building):
        if user_id not in self.civilizations:
            return False, MESSAGES['no_civilization']
        civ = self.civilizations[user_id]
        if building not in civ['buildings']:
            return False, MESSAGES['building_not_found']
        
        upgrade_cost = civ['buildings'][building] * 100
        if civ['gold'] < upgrade_cost:
            return False, MESSAGES['not_enough_gold']
        
        civ['gold'] -= upgrade_cost
        civ['buildings'][building] += 1
        return True, MESSAGES['building_upgraded'].format(building=building)

    def attack_city(self, user_id, target_civilization):
        if user_id not in self.civilizations:
            return False, MESSAGES['no_civilization']
        if target_civilization == '':
            return False, MESSAGES['missing_params']

        # Example attack logic
        victory = random.choice([True, False])
        if victory:
            civ = self.civilizations[user_id]
            bonus_troops = random.randint(10, 50)
            civ['troops'] += bonus_troops
            return True, MESSAGES['attack_won'].format(troops=bonus_troops)
        else:
            civ = self.civilizations[user_id]
            lost_troops = random.randint(10, 50)
            civ['troops'] = max(0, civ['troops'] - lost_troops)
            return False, MESSAGES['attack_lost'].format(troops=lost_troops)

    def complete_quest(self, user_id, quest_type):
        if user_id not in self.civilizations:
            return False, MESSAGES['no_civilization']
        if quest_type not in self.quests:
            return False, MESSAGES['invalid_quest']
        
        civ = self.civilizations[user_id]
        reward = self.quests[quest_type]
        civ['gold'] += reward
        civ['quests_completed'] += 1
        return True, MESSAGES['quest_completed'].format(reward=reward)

    def donate(self, user_id, amount):
        if user_id not in self.civilizations:
            return False, MESSAGES['no_civilization']
        if amount <= 0:
            return False, MESSAGES['invalid_amount']
        
        civ = self.civilizations[user_id]
        civ['gems'] += amount
        return True, MESSAGES['donation_received'].format(amount=amount)
