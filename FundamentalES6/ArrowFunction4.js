//define function for object
const hello = (name, umur) => ({
	status: 'OK',
	mesaage: `Hello ${name} umur ${umur}`
});

const result = hello('dimas', 25);
console.log(result);