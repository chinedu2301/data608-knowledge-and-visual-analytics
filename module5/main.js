// A function that reverses a word
function reversedWord(word) {
    return word.split('').reverse().join('')
  }


// Calculates multiples
function reversedWordOutput(){
    let output1 = document.getElementById("reversed_output");
    output1.innerHTML = reversedWord(document.getElementById('text_input_1').value);
}


// function that creates a table
function createTable(num){
    
    multiplesTable  = document.createElement('table');

    for(let i = 0; i < 5; i++){
        let tr = multiplesTable.insertRow();
        for(let j = 0; j < 4; j++){
			let td = tr.insertCell()
			td.innerHTML = num*(j+1)+num*4*(i)
        }
    }
    return(multiplesTable)
}


// function that appends to the table
function appendTable(){
	let output2 = document.getElementById("multiples_output");
	output2.innerHTML = ""
    output2.appendChild(createTable(document.getElementById('number_input_1').value));
}