const url = require('url');
const http = require('http');
const show = require('./show');
const fs = require('fs');

const express = require('express');
const router = express.Router();
const app = express();

// server files
app.use(express.static('public'));
app.use(express.static('public/layouts'));
app.use(express.static('public/layouts/assets'));
app.use(express.static('public/layouts/components'));
app.use(express.static('public/layouts/fonts/nunito'));
app.use(express.static('public.layouts/js'));

app.listen(80, () => {
	console.log('Listening on :80');
});

// send pages
app.use((req, res, next) => {
	show.showPage(res, req.url);
});
