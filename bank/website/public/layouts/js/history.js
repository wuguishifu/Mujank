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
		console.log(username);
		window.location.replace('/history/' + username);
	}
}
