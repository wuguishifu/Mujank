const fs = require('fs');
const csv = require('csv').parse;

const location = __dirname + '/public/layouts/'

function display_cards(res, username) {
	var user_id_map = JSON.parse(fs.readFileSync(__dirname + '/user_ids.json'));
	if (username in user_id_map['users']) {
		var user_id = user_id_map['users'][username];
		var mujank_db = JSON.parse(fs.readFileSync(__dirname + '/../../mujank_db.json'));
		var owned_card_ids = Object.keys(mujank_db['users'][user_id]['cards']);

		owned_cards = [];

		fs.createReadStream(__dirname + '/../../Mujank spreadsheet.csv')
			.on('error', () => {
				console.log('error');
			})
			.pipe(csv())
			.on('data', (row) => {
				if (owned_card_ids.includes(row[0])) {
					owned_cards.push(row);
				}
			})
			.on('end', () => {
				// send template with cards in owned_cards;
				res.sendFile(location + 'card_display.html');
			})

	} else {
		res.send(`<script>window.location.replace('/cards');
			alert("No user found!");</script>`);
	}
}

exports.display_cards = display_cards;
