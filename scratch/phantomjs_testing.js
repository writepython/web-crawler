var page = require('webpage').create();

console.log('Hello, world!');

var start = Date.now();

page.open('http://www.cuyoo.com/article-22418-1.html', function(status) {
    if (status !== 'success') {
	console.log('FAIL to load the address');
    } else {
	console.log(page.title);
	console.log(page.url);
	var t = Date.now() - start;
	console.log('Loading time ' + t + ' msec');
    }
    //page.render('cuyoo.png');
    phantom.exit();
});
