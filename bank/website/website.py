import csv
import datetime
import json
import os

import flask
import pandas as pd
from flask import Flask, request
from flask_cors import CORS

from waitress import serve

# set up flask server
app = Flask(__name__)
CORS(app)


class Card:
    def __init__(self, card_id: str, image_url: str, title: str, rating: int, tags: str):
        self.id = card_id
        self.image_url = image_url
        self.title = title
        self.rating = rating
        self.tags = tags

    def to_json(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'title': self.title,
            'rating': self.rating,
            'tags': self.tags
        }


spreadsheet_location = os.path.dirname(__file__) + '/../../Mujank spreadsheet.csv'
card_deck = {}
with open(spreadsheet_location) as mujank_spreadsheet:
    csvreader = csv.reader(mujank_spreadsheet)
    header = next(csvreader)
    for c in csvreader:
        if int(c[3]) != 0:
            card_deck[c[0]] = Card(c[0], f'{c[1]}', c[2], int(c[3]), c[4])


@app.route('/post_user_cards', methods=['POST'])
def get_user_cards():
    data = request.get_json()
    user_id = data['user_id']
    with open(os.path.dirname(__file__) + '/../../mujank_db.json') as json_file:
        data = json.load(json_file)
        if user_id not in data['users'].keys():
            response = flask.jsonify({
                'error': 'user-not-found',
                'cards': '-1'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            owned_cards = {}
            for card in data['users'][user_id]['cards'].keys():
                owned_cards[card] = card_deck[card].to_json()
            response = flask.jsonify({
                'error': 'none',
                'cards': owned_cards
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


@app.route('/post_card_search', methods=['POST'])
def card_search():
    data = request.get_json()
    query = data['query']
    match_cards = []
    for key in card_deck.keys():
        if query.lower() in card_deck[key].title.lower():
            match_cards.append(card_deck[key])
            print(card_deck[key].title)
    if len(match_cards) == 0:
        response = flask.jsonify({
            'error': 'no-cards-found',
            'cards': 'none'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        data = {'error': 'none', 'cards': {}}
        for card in match_cards:
            data['cards'][card.id] = card.to_json()
        response = flask.jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route('/post_user_bank', methods=['POST'])
def get_bank_hist():
    data = request.get_json()
    user_id: str = data['user_id']
    data = {'error': 'none', 'hist': {}}
    directory = os.path.dirname(__file__) + '/../date_history'
    data_found = False
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f) as csv_file:
                df = pd.read_csv(csv_file)
                if user_id in df.columns:
                    data_found = True
                    times = df.time
                    hist = df.get(user_id)
                    for i in range(len(times)):
                        time = datetime.datetime.strptime(times[i], '%m_%d_%Y %H_%M_%S')
                        data['hist'][time.strftime('%Y-%m-%dT%H:%M:%S')] = str(hist[i])
    with open(os.path.dirname(__file__) + '/../history.csv') as csv_file:
        df = pd.read_csv(csv_file)
        if user_id in df.columns:
            data_found = True
            times = df.time
            hist = df.get(user_id)
            for i in range(len(times)):
                time = datetime.datetime.strptime(times[i], '%m_%d_%Y %H_%M_%S')
                data['hist'][time.strftime('%Y-%m-%dT%H:%M:%S')] = str(hist[i])
    if data_found:
        return json.dumps(data)
    else:
        return {'error': 'user-not-found'}


@app.route('/post_user_id', methods=['POST'])
def get_user_id():
    username = request.get_json()['username']
    with open(os.path.dirname(__file__) + '/user_ids.json') as json_file:
        data = json.load(json_file)
        if username in data['users'].keys():
            response = flask.jsonify({
                'error': 'none',
                'user_id': data['users'][username]
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            response = flask.jsonify({
                'error': 'user-not-found',
                'user_id': '-1'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


@app.route('/test', methods=['GET'])
def test():
    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    ssl_context = ('mujank.com.crt', 'mujank.com_key.txt')
    app.run(port=8080, host='0.0.0.0', ssl_context=ssl_context)
