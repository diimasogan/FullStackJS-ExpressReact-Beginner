//let digunakan untuk deklarasi hanya dalam scope

var name = 'Dimas Agung Prakasa';

if (true) {
    let name = 'ogan';
    console.log(name); //<-- output "ogan"
}

console.log(name); // <-- output "dimas agung prakasa"