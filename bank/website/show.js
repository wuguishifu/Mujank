const fs = require('fs');
const csv = require('csv').parse;

const location = __dirname + '/public/layouts/'

function showPage(res, pathName) {
	if (pathName in contentMap) {
		res.sendFile(contentMap[pathName]);
	} else {
		res.sendFile(__dirname + '/public/layouts/404.html');
	}
}

const contentMap = {
	'/': location + 'main.html',
	'/submit': location	+ 'submit.html',
	'/cards/': location + 'cards.html',
	'404': location	+ '404.html',
	'/search': location + 'search.html',
	'/bank': location + 'bank.html'
}

exports.showPage = showPage;
