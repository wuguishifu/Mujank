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
	let uri = 'http://136.52.14.191:8080/user_id';
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
				displayCards(user_id, username);
			} else if (err === 'user-not-found') {
				alert('User not found!');
			}
		});
}

function displayCards(user_id, username) {
	let uri = 'http://136.52.14.191:8080/get_cards';
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
			document.getElementById('username-form').innerHTML = '';
			document.getElementById('title').innerHTML = `${username}'s Deck`;
			var container = document.getElementById('cards');

			let error = data.error;
			let cards = data.cards;

			let divs = '';

			for (const c of Object.keys(cards)) {
				let card = cards[c];
				let image_location = ('/img/' + card.image_url).replace(/ /g, '');
				divs += `<div class='card-${card.rating}'><h2>${card.title}</h2><img src='${image_location}' alt='${card.image_url}' width='400'></div>`
			}

			container.innerHTML = divs;

		})
}
