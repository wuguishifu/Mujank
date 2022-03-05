const url = require('url');
const http = require('http');
const show = require('./show');
const https = require('https');
const fs = require('fs');
const bodyParser = require('body-parser');
const moment = require('moment');
const csv = require('fast-csv');

var https_options = {
	key: fs.readFileSync('mujank.com_key.txt'),
	cert: fs.readFileSync('mujank.com.crt'),
	ca: [
		fs.readFileSync('mujank.com.p7b'),
		fs.readFileSync('mujank.com.ca-bundle')
	]
};

const express = require('express');
const router = express.Router();
const app = express();

var jsonParser = bodyParser.json();

var urlencodedParser = bodyParser.urlencoded({extended: false});

// server files
app.use(express.static('public'));
app.use(express.static('public/layouts'));
app.use(express.static('public/layouts/assets'));
app.use(express.static('public/layouts/components'));
app.use(express.static('public/layouts/fonts/nunito'));
app.use(express.static('public/layouts/js'));
app.use('/img', express.static('public/cards'));
app.use(bodyParser.json());

const bankHistoryDirectory = __dirname + '/../date_history';
const currHistory = __dirname + '/../history.csv';

httpsServer = https.createServer(https_options, app);
httpsServer.listen(443, () => {
	console.log('HTTPS Server running on port 443');
});

app.post('/post_user_id', urlencodedParser, (req, res) => {
	username = req.body.username;
	let rawUserData = fs.readFileSync(__dirname + '/user_ids.json');
	let users = JSON.parse(rawUserData);
	if (username in users.users) {
		res.send(JSON.stringify({error: 'none', user_id: users.users[username]}))
	} else {
		res.send(JSON.stringify({error: 'user-not-found', user_id: '-1'}));
	}
});

app.post('/post_user_cards', urlencodedParser, (req, res) => {
	user_id = req.body.user_id;
	let rawData = fs.readFileSync(__dirname + '/../../mujank_db.json');
	let database = JSON.parse(rawData);

	let ownedCards = Object.keys(database.users[user_id].cards);
	let toDisplay = [];

	if (user_id in database.users) {
		fs.createReadStream(__dirname + '/../../Mujank spreadsheet.csv')
			.pipe(csv.parse({headers: true}))
			.on('error', err => console.error(err))
			.on('data', row => {
				if (ownedCards.includes(row.id)) {
					let card = {
						id: row.id,
						image_url: row.file_name,
						title: row.title,
						rating: row.stars,
						tag: row.tag
					};
					toDisplay.push(card);
				}
			})
			.on('end', rowCount => {
				let data = {error: 'none', cards: {}};
				for (var card of toDisplay) {
					data.cards[card.id] = card;
				}
				res.send(JSON.stringify(data));
			});
	} else {
		res.send(JSON.stringify({error: 'user-not-found', cards: {}}));
	}
});

app.post('/post_user_bank', urlencodedParser, (req, res) => {
	user_id = req.body.user_id;
	const files = fs.readdirSync(bankHistoryDirectory);
	let count = 0;
	let numFiles = files.length + 1;

	var data = {error: 'none', hist: {}};
	let promises = [];

	for (const file of files) {
		fs.createReadStream(bankHistoryDirectory + '/' + file)
			.pipe(csv.parse({headers: true}))
			.on('error', err => console.error(err))
			.on('data', row => {
				let mom = moment(row.time, 'MM_DD_YYYY HH_mm_ss');
				let date = mom.toDate();
				data.hist[date] = row[user_id];
			})
			.on('end', rowCount => {
				count++;
				if (count === numFiles) {
					res.send(JSON.stringify(data));
				}
			});
	}

	fs.createReadStream(currHistory)
		.pipe(csv.parse({headers: true}))
		.on('error', err => console.error(err))
		.on('data', row => {
				let mom = moment(row.time, 'MM_DD_YYYY HH_mm_ss');
				let date = mom.toDate();
				data.hist[date] = row[user_id];
		})
		.on('end', rowCount => {
			count++;
			if (count === numFiles) {
				res.send(JSON.stringify(data));
			}
		})

});

app.post('/post_card_search', urlencodedParser, (req, res) => {
	query = req.body.query;
	let toDisplay = [];
	fs.createReadStream(__dirname + '/../../Mujank spreadsheet.csv')
		.pipe(csv.parse({headers: true}))
		.on('error', err => console.error(err))
		.on('data', row => {
			if (row.title.toLowerCase().includes(query.toLowerCase())) {
				let card = {
					id: row.id,
					image_url: row.file_name,
					title: row.title,
					rating: row.stars,
					tag: row.tag
				};
				toDisplay.push(card);
			}
		})
		.on('end', rowCount => {
			let data = {error: 'none', cards: {}};
			for (var card of toDisplay) {
				data.cards[card.id] = card;
			}
			res.send(JSON.stringify(data));
		});
});

// send other pages
app.use((req, res, next) => {
	show.showPage(res, req.url);
});
