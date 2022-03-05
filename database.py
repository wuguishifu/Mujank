import datetime
import json
import shutil
from datetime import date

import user

max_rolls = 3
file_path = 'mujank_db.json'


def backup():
    today = date.today()
    date_format = today.strftime('%m_%d_%Y')
    current_hour = datetime.datetime.now().hour
    current_min = datetime.datetime.now().minute
    destination = f'mujank_backup_{date_format}_{current_hour}_{current_min}'
    shutil.copy('mujank_db.json', f'db_backups/{destination}.json')


def save_data(data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def user_exists(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return user_id in data['users'].keys()


def add_user(user_id: str, user_name: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id] = {
            'num_cards': 0,
            'claimed': False,
            'num_rolls': 3,
            'displayed_card': 'c_id_-1',
            'cards': {},
            'wishlist': {},
            'inventory': {
                'items': {},
                'coins': 0
            }
        }
    save_data(data)
    with open('bank/website/user_ids.json') as json_file:
        data = json.load(json_file)
        data['users'][user_id] = user_name
        data['users'][user_name] = user_id
    with open('bank/website/user_ids.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def has_card(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return card_id in data['users'][user_id]['cards'].keys()


def get_num(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        if card_id in data['users'][user_id]['cards'].keys():
            return data['users'][user_id]['cards'][card_id]
        else:
            return 0


def get_cards(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['cards']


def add_card(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['num_cards'] += 1
        if data['users'][user_id]['displayed_card'] == 'c_id_-1':
            data['users'][user_id]['displayed_card'] = card_id
        if card_id in data['users'][user_id]['cards']:
            data['users'][user_id]['cards'][card_id] += 1
        else:
            data['users'][user_id]['cards'][card_id] = 1
    save_data(data)


def set_num(user_id: str, card_id: str, num: int):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['cards'][card_id] = num
    save_data(data)


def delete_card(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        del data['users'][user_id]['cards'][card_id]
    save_data(data)


def remove_card(user_id: str, card_id: str):
    needs_reset = False
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['num_cards'] -= 1
        if card_id in data['users'][user_id]['cards']:
            data['users'][user_id]['cards'][card_id] -= 1
            if data['users'][user_id]['cards'][card_id] == 0:
                needs_reset = True
                del data['users'][user_id]['cards'][card_id]
    save_data(data)
    if needs_reset:
        reset_displayed_card(user_id)


def check_claimed(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['claimed']


def set_claimed(user_id: str, claimed: bool):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['claimed'] = claimed
    save_data(data)


def get_num_rolls(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['num_rolls']


def dec_rolls(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['num_rolls'] -= 1
    save_data(data)


def reset_rolls(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['num_rolls'] = max_rolls
    save_data(data)


def set_displayed_card(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['displayed_card'] = card_id
    save_data(data)


def get_displayed_card(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['displayed_card']


def reset_displayed_card(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        displayed_card = data['users'][user_id]['displayed_card']
        if not has_card(user_id, displayed_card):
            if len(data['users'][user_id]['cards']) > 0:
                data['users'][user_id]['displayed_card'] = list(data['users'][user_id]['cards'])[0]
            else:
                data['users'][user_id]['displayed_card'] = 'c_id_-1'
    save_data(data)


def reset_all_timers():
    with open(file_path) as json_file:
        data = json.load(json_file)
        users = data['users'].keys()
        for u in users:
            reset_rolls(u)
            set_claimed(u, False)


def give_roll(user_id: str, amount=1):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['num_rolls'] += amount
    save_data(data)


def add_card_to_wishlist(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['wishlist'][card_id] = 1
    save_data(data)


def get_wishlist(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['wishlist']


def remove_card_from_wishlist(user_id: str, card_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['wishlist'][card_id] -= 1
        if data['users'][user_id]['wishlist'][card_id] == 0:
            del data['users'][user_id]['wishlist'][card_id]
    save_data(data)


def get_coins(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['inventory']['coins']


def add_coins(user_id: str, coins: int):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['inventory']['coins'] += coins
    save_data(data)


def remove_coins(user_id: str, coins: int):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['inventory']['coins'] -= coins
    save_data(data)


def get_items(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['inventory']['items']


def add_item(user_id: str, item_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        if item_id in data['users'][user_id]['inventory']['items']:
            data['users'][user_id]['inventory']['items'][item_id] += 1
        else:
            data['users'][user_id]['inventory']['items'][item_id] = 1
    save_data(data)


def remove_item(user_id: str, item_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['inventory']['items'][item_id] -= 1
        if data['users'][user_id]['inventory']['items'][item_id] == 0:
            del data['users'][user_id]['inventory']['items'][item_id]
    save_data(data)


def check_daily_coin_claim(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['users'][user_id]['inventory']['daily_coin_claim']


def set_daily_coin_claim(user_id: str, claimed: bool):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id]['inventory']['daily_coin_claim'] = claimed
    save_data(data)


def get_leaderboard():
    with open(file_path) as json_file:
        data = json.load(json_file)
        user_list = []
        for u in list(data['users']):
            user_list.append(user.User(u, data['users'][u]['inventory']['coins']))
    return sorted(user_list, reverse=True)


def reset_dailies():
    with open(file_path) as json_file:
        data = json.load(json_file)
        users = data['users'].keys()
        for u in users:
            data['users'][u]['inventory']['daily_coin_claim'] = False
    save_data(data)


def get_owners(card_id: str):
    card_owners = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        for u in list(data['users']):
            if card_id in data['users'][u]['cards'].keys():
                card_owners.append(u)
    return card_owners
