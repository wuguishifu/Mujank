import csv
import json
import shutil

bank_path = 'bank/history.csv'
database_path = 'mujank_db.json'


def update(time):
    rows = []

    # get current historical data
    with open(bank_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        fields = reader.fieldnames
        for row in reader:
            rows.append(row)
        if not fields:
            fields = ['time']

    # get current data
    with open(database_path, 'r') as json_file:
        data = json.load(json_file)
        new_data = {}
        for user_id in data['users']:
            if user_id not in fields:
                fields.append(user_id)
                for row in rows:
                    row.update({user_id: 0})
                    print(row)
            new_data.update({user_id: data['users'][user_id]['inventory']['coins']})
        new_data.update({'time': time})
        rows.append(new_data)

    with open(bank_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def backup(date):
    shutil.move('bank/history.csv', f'bank/date_history/history_{date}.csv')
    new_file = open('bank/history.csv', 'x')
    new_file.close()
