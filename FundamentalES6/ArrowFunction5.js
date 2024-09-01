//define function
const hello = name => {

	if(!name) {
		console.log('Name is required');
	}
	
	return `Hello ${name}`;

}
const result = hello();//output Name is required

const greeting = hello('Dimas'); //output dimas
console.log(greeting);