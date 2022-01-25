import json

with open('mujank_db.json') as json_file:
    data = json.load(json_file)
    users = data['users']
    for user in list(users):
        user_data = users[user]
        if 'daily_coin_claim' not in user_data['inventory']:
            user_data['inventory']['daily_coin_claim'] = False

with open('mujank_db.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
