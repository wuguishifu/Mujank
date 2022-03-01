const fs = require('fs');
const csv = require('csv').parse;
const path = require('path');

const location = __dirname + '/public/layouts/'

function display_cards(res, username) {
	var user_id_map = JSON.parse(fs.readFileSync(__dirname + '/user_ids.json'));
	if (username in user_id_map['users']) {
		var user_id = user_id_map['users'][username];
		var mujank_db = JSON.parse(fs.readFileSync(__dirname + '/../../mujank_db.json'));
		var owned_card_ids = Object.keys(mujank_db['users'][user_id]['cards']);

		owned_cards = [];

		let cards = "";

		fs.createReadStream(__dirname + '/../../Mujank spreadsheet.csv')
			.on('error', () => {
				console.log('error');
			})
			.pipe(csv())
			.on('data', (row) => {
				if (owned_card_ids.includes(row[0])) {
					owned_cards.push(row);
					let image_location = ('/img/' + row[1]).replace(/ /g, '');
					cards += `<div class='card-${row[3]}'><h2>${row[2]}</h2><img src="${image_location}" alt="${row[1]}" width="400"></div>`
				}
			})
			.on('end', () => {
				// send template with cards in owned_cards;
				res.send(card_display.replace('{{cards}}', cards).replace('{{Name}}', `${username}'s Cards`));
			})

	} else {
		res.send(`<script>window.location.replace('/cards');
			alert("No user found!");</script>`);
	}
}

card_display = `<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="/card_display.css">
	<link rel="shortcut icon" type="image/x-icon" href="/assets/favicon.ico">
	<title>Cards</title>
</head>

<body>
	<div class="topnav">
		<a href="/">Home</a>
		<a href="/cards">Cards</a>
		<a href="/search">Card Search</a>
	</div>

	<div class="center">
		<div class="header">
			<h1>{{Name}}</h1>
		</div>
	</div>

	<div class="center">
		<div class="card_box", align="center", id="cards">
			{{cards}}
		</div>
	</div>

	<script src="/js/card_display.js"></script>
</body>


</html>`

exports.display_cards = display_cards;
