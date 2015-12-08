var finalhandler = require('finalhandler')
var http = require('http')
//var fs = require('fs')
var serveStatic = require('serve-static')
var motionService = require('./motion-service')

// configuration
var port = 3000;
var dataDirectory = "data/";
var serve = serveStatic("client/",{});
var motionAPI = /\/api\/motion\/([0-9])+/g;
var server = http.createServer(function(req, res){
    console.log(req.method+' request for: '+req.url);
    if (req.method === "POST" && req.url.match(motionAPI)) {
      var id = req.url.split('/')[req.url.split('/').length-1];
      console.log("id: "+id);
      var body="";
      req.on('data', function(data) {
          body+= data;
      });
      req.on('end',function() {
          console.log('srv.js - received POST body: '+body);
          motionService.updateData(dataDirectory, id, body);
      });
      var postResponse = "post received";
      res.writeHead(200, {
          'Content-Type' : 'application/json',
          'Content-Length': postResponse.length});
      res.end(postResponse);
    } else {
      var done = finalhandler(req, res);
      serve(req, res, done);
    }
});

console.log("Starting server on: http://localhost:"+port);
server.listen(port);
