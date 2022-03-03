var uri_header = 'https://136.52.14.191:80/';

var queryEntry = document.getElementById('username-entry');
queryEntry.addEventListener('keypress', function (e) {
	if (e.key === 'Enter') {
		findCards(queryEntry.value);
	}
})

document.getElementById('submit-button').addEventListener('click', function (e) {
	findCards(queryEntry.value);
});

container = document.getElementById('cards');

function findCards(query) {
	if (query.length === 0) {
		alert('Please enter a search!')
	} else {
		let uri = uri_header + 'post_card_search';
		fetch(uri, {
			method: 'POST',
			mode: 'cors',
			cache: 'no-cache',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({query: query})
		})
			.then(response => response.json())
			.then((data) => {
				let err = data.error;
				if (err === 'none') {
					displayCards(data, query);
				} else {
					alert('No cards found!');
				}
			});
	}
}

function displayCards(data, query) {
	let divs = '';
	for (const c in data.cards) {
		let card = data.cards[c];
		let image_location = ('/img/' + card.image_url).replace(/ /g, '');
		divs += `<div class='card-${card.rating}'><h2>${card.title}</h2><img src='${image_location}' alt='${card.image_url}' width='400'></div>`
	}
	container.innerHTML = divs;
}
