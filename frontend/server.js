const express = require('express')
const serveStatic = require('serve-static')
const history = require('connect-history-api-fallback');

const path = require('path')
const app = express()
const staticFileMiddleware = express.static(path.join(__dirname + '/dist'));

app.use(staticFileMiddleware);
app.use(history({
    index: '/index.html',
    disableDotRule: true,
    verbose: true
}));
app.use(staticFileMiddleware);

app.get('/', function(req, res) {
    res.render(path.join(__dirname + '/dist/index.html'));
});

var server = app.listen(process.env.PORT || 8080, function() {
    var port = server.address().port;
    console.log("App now running on port", port);
});

// var express = require('express')
// var history = require('connect-history-api-fallback')
// var path = require('path')
// var serveStatic = require('serve-static')


// var app = express()

// // Use a fallback for non-root routes (required for Vue router)
// //   NOTE: History fallback must be "used" before the static serving middleware!
// app.use(history({
//     // OPTIONAL: Includes more verbose logging
//     verbose: true
// }))

// // Serve static assets from the build files (images, etc)
// app.use(serveStatic(path.join(__dirname, '/dist')))

// var port = process.env.PORT || 8080

// app.listen(port, () => {
//     console.log('Server started at http://localhost:8080')
// })

// const express = require('express')
// const serveStatic = require('serve-static')
// const path = require('path')
// const app = express()
// app.use('/', serveStatic(path.join(__dirname, '/dist')))
// const port = process.env.PORT || 8080
// console.log("port = " + port)
// app.listen(port)