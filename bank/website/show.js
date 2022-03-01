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

function showHistory(res, username) {
	var user_id_map = JSON.parse(fs.readFileSync(__dirname + '/user_ids.json'));
	if (username in user_id_map['users']) {
		var user_id = user_id_map['users'][username.toString()];
		var mujank_db = JSON.parse(fs.readFileSync(__dirname + '/../../mujank_db.json'));
		console.log(mujank_db['users'][user_id]);
	} else {
		res.send(`<script>window.location.replace('/history');
			alert("No user found!");</script>`);
	}
}

const contentMap = {
	'/': location + 'main.html',
	'/submit': location	+ 'submit.html',
	'/cards': location + 'cards.html',
	'/history': location + 'history.html',
	'404': location	+ '404.html',
	'no_user': location + 'no_user.html',
	'/search': location + 'search.html'
}

exports.showPage = showPage;
