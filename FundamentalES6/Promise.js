//define variable
let done = true;

//define a promise
const task = new Promise((resolve, reject) => {

	if(done) {
		
		resolve('Task berhasil diselesaikan');
		
	} else {
		
		reject('Task belum diselesaikan');
	
	}

});

// run promise
console.log(task); // <-- ouput "Task berhasil diselesaikan"