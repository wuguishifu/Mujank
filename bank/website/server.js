const url = require('url');
const http = require('http');
const show = require('./show');
const https = require('https');
const card_display = require('./card_display');
const card_search = require('./card_search')
const fs = require('fs');

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

// server files
app.use(express.static('public'));
app.use(express.static('public/layouts'));
app.use(express.static('public/layouts/assets'));
app.use(express.static('public/layouts/components'));
app.use(express.static('public/layouts/fonts/nunito'));
app.use(express.static('public/layouts/js'));
app.use('/img', express.static('public/cards'));

httpsServer = https.createServer(https_options, app);
httpsServer.listen(443, () => {
	console.log('HTTPS Server running on port 443');
});

app.get('/cards', (req, res) => {
	if (Object.keys(req.query).length === 0) {
		show.showPage(res, '/cards');
	} else {
		card_display.display_cards(res, req.query.user);
	}
});

app.get('/search', (req, res) => {
	if (Object.keys(req.query).length === 0) {
		show.showPage(res, '/search');
	} else {
		card_search.search_cards(res, req.query.query)
	}
});

// send pages
app.use((req, res, next) => {
	show.showPage(res, req.url);
});
