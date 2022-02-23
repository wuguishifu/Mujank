const express = require('express');
const app = express();

const url = require('url');
const http = require('http');
const show = require('./show');

// server files
app.use(express.static('public'));
app.use(express.static('public/layouts'));
app.use(express.static('public/layouts/assets'));
app.use(express.static('public/layouts/components'));
app.use(express.static('public/layouts/fonts/nunito'));

app.listen(80, () => {
	console.log('Listening on :80');
});

// send pages
app.get('*', (req, res) => {
	if (req.url != '/favicon.ico') {
		show.showPage(res, req.url);
	}
});
