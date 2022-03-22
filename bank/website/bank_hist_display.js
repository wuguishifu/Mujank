function displayBankHistory(res, req) {
	var displayFunction = `
	let uri = 'https://mujank.com/' + 'post_user_bank';
	fetch(uri, {
		method: 'POST',
		mode: 'cors',
		cache: 'no-cache',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({user_id: ${req.query['user_id']}})
	})
		.then(response => response.json())
		.then((data) => {
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
		});
`

	res.send(bankHistHTML.replace('{{code_here}}', displayFunction));
}

const bankHistHTML = `<!DOCTYPE html>
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
		{{code_here}}
	}
	window.onload = codeAddress;
	</script>
</body>


</html>`;

exports.displayBankHistory = displayBankHistory;