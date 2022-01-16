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


def user_exists(user_id: int):
    if db.child(f'users/{user_id}').get().val():
        return True
    else:
        return False


def add_user(user_id: int):
    db.child(f'users/{user_id}').set({'num_cards': 0})


def card_owned(card_id: int):
    users = db.child(f'users').get().val()
    for u in users:
        if card_id in get_cards(u):
            return True
    return False


def get_cards(user_id: int):
    cards = db.child(f'users/{user_id}/cards').get().val()
    cards_list = []
    if cards:
        for key, value in cards.items():
            cards_list.append(value['id'])
        cards_list.sort()
        return cards_list
    else:
        return []


def add_card(user_id: int, card_id: int):
    cards = get_cards(user_id)
    exists = False
    if cards:
        for card in cards:
            if card == card_id:
                exists = True
                break

    if exists:
        return False
    else:
        num_cards = int(db.child(f'users/{user_id}/num_cards').get().val())
        num_cards += 1
        db.child(f'users/{user_id}/cards').push({'id': card_id})
        db.child(f'users/{user_id}').update({'num_cards': num_cards})
        return True


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
