const fs = require('fs');
const csv = require('csv').parse;

const location = __dirname + '/public/layouts/'

function showPage(res, pathName) {
	if (pathName == 'bank_hist') {
		res.send(bank_hist_html);
	}
	else if (pathName in contentMap) {
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

const bank_hist_html = `<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="/bank.css">
	<link rel="shortcut icon" type="image/x-icon" href="/assets/favicon.ico">
	<script src='https://cdn.plot.ly/plotly-2.9.0.min.js'></script>
	<title>Bank</title>
</head>

<body>
	<div class="center" id="center-div">
		<div id="bank-plot" align="center"></div>
	</div>
	<script type="text/javascript">
	function codeAddress() {

	}
	window.onload = codeAddress;
	</script>
</body>


</html>`

exports.showPage = showPage;
