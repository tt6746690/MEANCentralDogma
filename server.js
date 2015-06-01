var colors = require('colors');
var morgan = require('morgan');
var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var cp = require('child_process');
var port = process.argv[2];
var app = express();


// ====Middleware===
// CORS
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

//morgan
app.use(morgan(
    ':method'.bold.cyan + 
    ' |:url'.bold.green +
    ' |status:' + ':status'.bold.blue +
    ' |size: ' + ':res[content-length]'.bold.magenta + 'bits'.bold +
    ' |response time: ' + ':response-time'.bold.yellow + 'ms'.bold
	));


//Mongoose
var dburl = 'mongodb://localhost/test';// where is this test database located on drive?
mongoose.connect(dburl);
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function (callback) {
    console.log('connect to database');
});
var dogmas = mongoose.Schema({
        dna: String,
        protein: String
    })
var Dogmamodel = mongoose.model('dogma', dogmas);

//serve public files
app.use(express.static('public'));

//---Routes---
app.get('/ProteintoDNA', function(req, res){
    res.send('get DNA from protein sequence:');
})

app.get('/history', function(req, res){
	Dogmamodel.find(function(err, docs){
        if (err)
            console.log(err);
        console.log('history sent'.blue);
        res.send(docs);
    })
})

app.post('/DNAtoProtein', function(req, res){
	var reqsequence = req.body.sequence;
    var catcher = cp.spawn('python3', ['sequence.py', reqsequence]);
    var results = {
        transformed: null,
        errorlog: null,
        exitcode: null
    }
    catcher.stdout.on('data', function(data){
        results.transformed = data.toString();
    })
        catcher.stderr.on('data', function(data){
            results.errorlog = data.toString();
        })
        catcher.on('close', function(code){
        results.exitcode = code;
          if(code === 0){
            var instance = new Dogmamodel({
                dna: reqsequence,
                protein: results.transformed
            })
            instance.save(function(err){
                console.log('saved to database');
            })
        }
        res.send(results);
    })
})



app.listen(port);

console.log('express server listening on port ' + port);
