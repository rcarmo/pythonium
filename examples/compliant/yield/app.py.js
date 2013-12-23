frak = function *() {
    yield 42;
}

var fuuu = function *() {
    console.log('fuuuu');
    a = yield frak(); 
}
var f = fuuu()
f.next()
f.send(undefined)
