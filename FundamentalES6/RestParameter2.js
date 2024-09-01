function sum(initVal, ...rest) {
    let sum = 0;
    for (let number of rest) sum += number;
    return initVal + sum;
  }
  
  let x = sum(10, 5); // <-- output "15"

  console.log(x);