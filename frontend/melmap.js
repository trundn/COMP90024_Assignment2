var http = require("http");
var fs = require("fs");

http.createServer(function (request, response) {
    res = response.writeHead(200,  {"Content-Type": "text/html"});
    var myRS = fs.createReadStream(__dirname+ "/index - leaflet.html", "utf8");
    myRS.pipe(res);
}).listen(8081);

console.log("Server is running at http://127.0.0.1:8081");
