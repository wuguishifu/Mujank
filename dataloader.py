import os
import collections

import dotenv
import pyrebase

dotenv.load_dotenv()

firebase_config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DB_URL'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
}

firebase = pyrebase.initialize_app(config=firebase_config)
db = firebase.database()


max_rolls = 3


def user_exists(user_id: int):
    if db.child(f'users/{user_id}').get().val():
        return True
    else:
        return False


def add_user(user_id: int):
    db.child(f'users/{user_id}').set({'num_cards': 0, 'claimed': False, 'num_rolls': 3})


def get_num(user_id: int, card_id: int):
    cards = get_cards(user_id)
    exists = False
    if cards:
        for card in cards:
            if int(card) == card_id:
                exists = True
                break
    if exists:
        return int(db.child(f'users/{user_id}/cards/{card_id}/num').get().val())
    else:
        return 0


def get_cards(user_id: int):
    cards = db.child(f'users/{user_id}/cards').get().each()
    cards_list = []
    if cards:
        for card in cards:
            cards_list.append(int(card.key()))
        cards_list.sort()
        return cards_list
    else:
        return []


def add_card(user_id: int, card_id: int):
    cards = get_cards(user_id)
    exists = False
    if cards:
        for card in cards:
            if int(card) == card_id:
                exists = True
                break

    num_cards = int(db.child(f'users/{user_id}/num_cards').get().val())
    if exists:
        num = int(db.child(f'users/{user_id}/cards/{card_id}/num').get().val())
        db.child(f'users/{user_id}/cards/{card_id}').set({'num': (num + 1)})
        pass
    else:
        db.child(f'users/{user_id}/cards/{card_id}').set({'num': 1})
    num_cards += 1
    db.child(f'users/{user_id}').update({'num_cards': num_cards})


def remove_card(user_id: int, card_id: int):
    cards_dict = collections.OrderedDict = db.child(f'users/{user_id}/favorites').get().val()
    card_key = 0
    exists = False
    for key, value in cards_dict.items():
        if value['id'] == card_id:
            card_key = key
            exists = True
            break

    # remove the card
    if exists:
        db.child(f'users/{user_id}/favorites').child(card_key).remove()
        num_cards = int(db.child(f'users/{user_id}/num_cards').get().val())
        num_cards -= 1
        db.child(f'users/{user_id}').update({'num_cards': num_cards})
        return True
    else:
        return False


def check_claimed(user_id: int):
    return bool(db.child(f'users/{user_id}/claimed').get().val())


def set_claimed(user_id: int, claimed: bool):
    db.child(f'users/{user_id}').update({'claimed': claimed})


def get_num_rolls(user_id: int):
    return int(db.child(f'users/{user_id}/num_rolls').get().val())


def dec_rolls(user_id: int):
    num = get_num_rolls(user_id) - 1
    db.child(f'users/{user_id}').update({'num_rolls': num})


def reset_rolls(user_id: int):
    db.child(f'users/{user_id}').update({'num_rolls': max_rolls})

