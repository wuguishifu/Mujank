import json

max_rolls = 3
file_path = 'mujank_db.json'


def save_data(data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def user_exists(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return user_id in data['users'].keys()


def add_user(user_id: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data['users'][user_id] = {
            'num_cards': 0,
            'claimed': False,
            'num_rolls': 3,
            'displayed_card': 'c_id_-1',
            'cards': {},
            'wishlist': {}
        }
    save_data(data)


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
        for user in users:
            reset_rolls(user)
            set_claimed(user, False)


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
