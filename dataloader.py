import os
import collections
from enum import Enum

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


class ReturnValues(Enum):
    false = 0
    true = 1

    does_not_exist = 0
    exists = 1

    not_added = 0
    added = 1

    def __int__(self):
        return self.value


def guild_exists(guild_id: int):
    if db.child(f'guilds/{guild_id}').get().val():
        return ReturnValues.exists
    else:
        return ReturnValues.does_not_exist


def add_guild(guild_id: int):
    db.child(f'guilds/{guild_id}').set({'prefix': '*'})


def get_guild_prefix(guild_id: int):
    if not guild_exists(guild_id):
        add_guild(guild_id)
    return db.child(f'guilds/{guild_id}/prefix').get().val()


def change_guild_prefix(guild_id: int, prefix: str):
    db.child(f'guilds/{guild_id}').update({'prefix': prefix})


def user_exists(user_id: int):
    if db.child(f'users/{user_id}').get().val():
        return ReturnValues.exists
    else:
        return ReturnValues.does_not_exist


def add_user(user_id: int):
    db.child(f'users/{user_id}').set({'num_cards': 0})


def get_cards(user_id: int):
    cards = db.child(f'users/{user_id}/cards').get().val()
    cards_list = []
    if cards:
        for key, value in cards.items():
            cards_list.append(value['id'])
        cards_list.sort()
        return cards_list
    else:
        return None


def add_card(user_id: int, card_id: int):
    cards = get_cards(user_id)
    exists = False
    if cards:
        for card in cards:
            if card == card_id:
                exists = True
                break

    if exists:
        return ReturnValues.not_added
    else:
        num_cards = int(db.child(f'users/{user_id}/num_cards').get().val())
        num_cards += 1
        db.child(f'users/{user_id}/cards').push({'id': card_id})
        db.child(f'users/{user_id}').update({'num_cards': num_cards})
        return ReturnValues.added


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
        return ReturnValues.true
    else:
        return ReturnValues.false
