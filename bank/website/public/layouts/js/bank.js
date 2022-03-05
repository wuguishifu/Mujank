var uri_header = 'http://mujank.com/';

var usernameEntry = document.getElementById('username-entry');
usernameEntry.addEventListener('keypress', function (e) {
	if (e.key === 'Enter') {
		findUser(usernameEntry.value);
	}
})

document.getElementById('submit-button').addEventListener('click', function (e) {
	findUser(usernameEntry.value);
});

function findUser(username) {
	if (username.length === 0) {
		alert('Please enter your username.');
	} else {
		getUserID(username);
	}
}

function getUserID(username) {
	let uri = uri_header + 'post_user_id';
	fetch(uri, {
		method: 'POST',
		cache: 'no-cache',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({username: username})
	})
		.then(response => response.json())
		.then((data) => {
			let err = data.error;
			if (err === 'none') {
				let user_id = data.user_id;
				displayBankHistory(user_id, username);
			} else if (err === 'user-not-found') {
				alert('User not found!');
			}
		})
}

function displayBankHistory(user_id, username) {
	let uri = uri_header + 'post_user_bank';
	fetch(uri, {
		method: 'POST',
		mode: 'cors',
		cache: 'no-cache',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({user_id: user_id})
	})
		.then(response => response.json())
		.then((data) => {
			document.getElementById('entry-form').innerHTML = '';
			document.getElementById('title').innerHTML = `${username}'s Bank History`;
			var bankPlot = document.getElementById('bank-plot');

			let err = data.error;
			let hist = data.hist;
			let times = [];
			let vals = [];
			let dataPoints = [];

			for ([key, val] of Object.entries(hist)) {
				dataPoints.push({date: new Date(key), val: val});
			}
			dataPoints.sort((a, b) => {
				let d1 = a.date;
				let d2 = b.date;
				return d1 - d2;
			});
			for (var i = 0; i < dataPoints.length; i++) {
				times.push(dataPoints[i].date);
				vals.push(dataPoints[i].val);
			}

			var data = [{
				x: times, y: vals, type: 'line'
			}];

			var layout = {
				autosize: false,
				width: 3*window.innerWidth/4,
				height: 3*window.innerHeight/4,
				xaxis: {title: 'Date'},
				yaxis: {title: 'Jankcoin Balance'}
			};

			Plotly.newPlot(bankPlot, data, layout);
		})
}
