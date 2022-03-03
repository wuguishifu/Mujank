const fs = require('fs');
const csv = require('csv').parse;
const path = require('path');

const location = __dirname + '/public/layouts/';

function search_cards(res, query) {
	let cards = "";
	fs.createReadStream(__dirname + '/../../Mujank spreadsheet.csv')
		.on('error', () => {
			console.log('error');
		})
		.pipe(csv())
		.on('data', (row) => {
			if ((row[2].toLowerCase()).includes(query.toLowerCase())) {
				let image_location = ('/img/' + row[1]).replace(/ /g, '');
				cards += `<div class='card-${row[3]}'><h2>${row[2]}</h2><img src="${image_location}" alt="${row[1]}" width="400"></div>`
			}
		})
		.on('end', () => {
			res.send(search_display.replace('{{cards}}', cards));
		})
}


search_display = `<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="/search_display.css">
	<link rel="shortcut icon" type="image/x-icon" href="/assets/favicon.ico">
	<title>Search</title>
</head>

<body>
	<div class="topnav">
		<a href="/">Home</a>
		<a href="/cards">Cards</a>
		<a href="/bank">Bank</a>
		<a href="/search">Card Search</a>
	</div>

	<div class="center">
		<div class="header">
			<h1>Search Results</h1>
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

exports.search_cards = search_cards;
