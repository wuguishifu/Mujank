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


max_rolls = 100


def user_exists(user_id: int):
    if db.child(f'users/{user_id}').get().val():
        return True
    else:
        return False


def add_user(user_id: int):
    db.child(f'users/{user_id}').set({'num_cards': 0, 'claimed': False, 'num_rolls': 3, 'displayed_card': 'c_id_-1'})


def get_num(user_id: int, card_id: str):
    if db.child(f'users/{user_id}/cards/{card_id}').get().val():
        return int(db.child(f'users/{user_id}/cards/{card_id}').get().val())
    else:
        return 0


def get_cards(user_id: int):
    cards = db.child(f'users/{user_id}/cards').get()
    if cards.pyres:
        cards_list = []
        for pyre in cards.pyres:
            cards_list.append(pyre)
            pass
        return cards_list
    else:
        return []


def add_card(user_id: int, card_id: str):
    num_cards = int(db.child(f'users/{user_id}/num_cards').get().val())
    if num_cards == 0:
        set_displayed_card(user_id, card_id)
    if db.child(f'users/{user_id}/cards/{card_id}').get().val():
        num = int(db.child(f'users/{user_id}/cards/{card_id}').get().val())
        db.child(f'users/{user_id}/cards').update({card_id: (num + 1)})
        pass
    else:
        db.child(f'users/{user_id}/cards').update({card_id: 1})
    num_cards += 1
    db.child(f'users/{user_id}').update({'num_cards': num_cards})


def set_num(user_id: int, card_id: str, num: int):
    db.child(f'users/{user_id}/cards').update({card_id: num})


def delete_card(user_id: int, card_id: str):
    db.child(f'users/{user_id}/cards/{card_id}').remove()


def remove_card(user_id: int, card_id: str):
    cards = get_cards(user_id)
    if card_id in [item.key() for item in cards]:
        num = get_num(user_id, card_id) - 1
        if num > 0:
            set_num(user_id, card_id, num)
        else:
            delete_card(user_id, card_id)


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


def set_displayed_card(user_id: int, card_id: str):
    db.child(f'users/{user_id}').update({'displayed_card': card_id})


def get_displayed_card(user_id: int):
    return db.child(f'users/{user_id}/displayed_card').get().val()


def reset_displayed_card(user_id: int):
    cards = get_cards(user_id)
    db.child(f'users/{user_id}').update({'displayed_card': cards[0].key()})

