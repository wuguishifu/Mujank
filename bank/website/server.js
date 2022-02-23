const express = require('express');
const app = express();

const url = require('url');
const http = require('http');
const show = require('./show');

// server files
app.use(express.static('public'));
app.use(express.static('public/layouts'));

app.listen(3000, () => {
	console.log('Listening on :3000');
});

// send main page
app.get('/', (req, res) => {
	show.showPage(res, '/');
});

// send 404 page - must be last
app.get('*', (req, res) => {
	show.showPage(res, '*');
});
