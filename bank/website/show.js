const fs = require('fs');

const location = __dirname + '/public/layouts/'

function showPage(res, pathName) {
	if (pathName.includes('/history/')) {
		showHistory(res, pathName.substring(9));
	} else {
		if (pathName in contentMap) {
			res.sendFile(contentMap[pathName]);
		} else {
			res.sendFile(__dirname + '/public/layouts/404.html');
		}
	}
}

function showHistory(res, username) {
	var user_id_map = JSON.parse(fs.readFileSync(__dirname + '/user_ids.json'));
	if (username in user_id_map['users']) {
		var user_id = user_id_map['users'][username.toString()];
		var mujank_db = JSON.parse(fs.readFileSync(__dirname + '/../../mujank_db.json'));
		for (var id in mujank_db['users']) {
			console.log(id + ", " + user_id.toString());
			if (id === user_id) {
				console.log(mujank_db['users'][id]);
			}
		}
	} else {
		res.send(`<script>window.location.replace('/history');
			alert("No user found!");</script>`);
	}
}

const contentMap = {
	'/': location + 'main.html',
	'/submit': location	+ 'submit.html',
	'/history': location + 'history.html',
	'404': location	+ '404.html',
	'no_user': location + 'no_user.html'
}

exports.showPage = showPage;
