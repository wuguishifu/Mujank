var location = __dirname + '/public/layouts/'

function showPage(res, pathName) {
	if (pathName in contentMap) {
		res.sendFile(contentMap[pathName]);
	} else {
		res.sendFile(contentMap['404']);
	}
}

const contentMap = {
	'/': location + 'main.html',
	'404': location + '404.html'
}

exports.showPage = showPage;
