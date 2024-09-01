//var digunakan untuk deklarasi diluar scope dan dalam scope

var name = 'Dimas Agung Prakasa';

if (true) {
    var name = 'ogan';
    console.log(name); //<-- output "ogan"
}

console.log(name); // <-- output "ogan"