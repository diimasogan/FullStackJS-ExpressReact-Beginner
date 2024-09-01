//spread operator for gabungin array

//define array 1
const arr1 = [1, 2, 3];

//define array 2
const arr2 = [4, 5, 6];

//define array 3
const arr3 = [...arr1, ...arr2];

//print array 3
console.log(arr3); // <-- [1, 2, 3, 4, 5, 6];