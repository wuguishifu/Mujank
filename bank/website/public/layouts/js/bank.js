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
	let uri = 'http://127.0.0.1:5000/user_id';
	fetch(uri, {
		method: 'POST',
		mode: 'cors',
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
				alert('User not found!')
			}
		})
}

function displayBankHistory(user_id, username) {
	let uri = 'http://127.0.0.1:5000/bank_hist';
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
			times = [];
			vals = [];

			for ([key, val] of Object.entries(hist)) {
				times.push(new Date(key));
				vals.push(val);
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
