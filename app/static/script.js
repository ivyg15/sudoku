var isPencil = false;
var activeCell = null;

// create puzzle grid
var puzzleContainer = document.getElementById("puzzleContainer");
var puzzle = document.createElement("table");
for (let i = 0; i < 9; i++){
  var row = document.createElement("tr");
  for (let j = 0; j < 9; j++){
    var cell = document.createElement("td")
    category = ""
    if (i % 3 === 0){
      category += "top"
    }
    if (i % 3 === 2){
      category += "bottom"
    }
    if (j % 3 === 0){
      category += "left"
    }
    if (j % 3 === 2){
      category += "right"
    }
    cell.setAttribute("class", category);
    cell.setAttribute("id", ((i+1)*10+j+1).toString());
    
    var valContainer = document.createElement("div");
    valContainer.setAttribute("class", "valContainer");
    valContainer.setAttribute("id", "v"+cell.id);
    cell.appendChild(valContainer);
    
    var pencilContainer = document.createElement("div");
    pencilContainer.setAttribute("class", "pencilContainer");
    for (let pencilI = 0; pencilI < 3; pencilI++){
      for (let pencilJ = 0; pencilJ < 3; pencilJ++){
        var pencil = document.createElement("div");
        pencil.setAttribute("class", "pencil");
        pencil.setAttribute("id", ((i+1)*10+j+1).toString() + ((pencilI)*3+pencilJ+1).toString());
        pencilContainer.appendChild(pencil);
      }
    }
    cell.appendChild(pencilContainer);
    
    cell.addEventListener("click", function(e){
      if (activeCell !== null){
        neighborColors(activeCell.id, "white");
      }
      if (e.target.className === "pencil"){
        activeCell = e.target.parentElement.parentElement;
      }
      else if (e.target.className === "pencilContainer"){
        activeCell = e.target.parentElement;
      }
      neighborColors(activeCell.id, "lightcyan");
      activeCell.style.backgroundColor = "rgb(182, 250, 250)";
    });
    row.appendChild(cell);
  }
  puzzle.appendChild(row);
}
puzzleContainer.appendChild(puzzle);

// font sizes
for (let i = 1; i < 10; i++){
  for (let j = 1; j < 10; j++){
    for (let k = 1; k < 10; k++){
      var pencil = document.getElementById(i.toString()+j.toString()+k.toString());
      pencil.style.fontSize = pencil.clientWidth*0.8.toString()+"px";
      pencil.style.textAlign = "center";
    }
  }
}

for (let i = 1; i < 10; i++){
  for (let j = 1; j < 10; j++){
    var cell = document.getElementById("v"+i.toString()+j.toString());
    cell.style.fontSize = cell.clientWidth*0.7.toString()+"px";
    cell.style.textAlign = "center";
  }
}

document.addEventListener("keydown", handleKeyDown);

function handleKeyDown(e){
  var val = e.key;
  if (/^\d+$/.test(val) || val === "Backspace"){
    editCell(val);
  }
  else if (val === "ArrowDown" || val === "ArrowUp" || val === "ArrowLeft" || val === "ArrowRight"){
    e.preventDefault();
    move(val);
  }
}

function editCell(val){
  if (isPencil && document.getElementById("v"+activeCell.id).innerHTML === "" && /^\d+$/.test(val)){
    var pencil = document.getElementById(activeCell.id+val);
    if (pencil.innerHTML === ""){
      pencil.innerHTML = val;
    }
    else{
      pencil.innerHTML = "";
    }
  }
    
  else if (!(isPencil) && /^\d+$/.test(val)){
    for (let i = 1; i < 10; i++){
      var id = activeCell.id+i.toString();
      var pencil = document.getElementById(id);
      pencil.setAttribute("hidden", "hidden");
    }
    var center = document.getElementById("v"+activeCell.id);
    center.innerHTML = val;
  }
  else if (!(isPencil) && val === "Backspace"){
    var center = document.getElementById("v"+activeCell.id);
    center.innerHTML = "";
    for (let i = 1; i < 10; i++){
      var pencil = document.getElementById(activeCell.id+i.toString());
      pencil.removeAttribute("hidden");
    }
  }
}

function move(val){
  if (activeCell === null) {
    return;
  }
  var activeX = parseInt(activeCell.id)%10;
  var activeY = Math.floor(parseInt(activeCell.id)/10);
  if (val === "ArrowDown"){
    if (activeY < 9){
      neighborColors(activeY.toString()+activeX.toString(), "white")
      activeY += 1;
      activeCell = document.getElementById(activeY.toString()+activeX.toString())
      neighborColors(activeCell.id, "lightcyan")
      activeCell.style.backgroundColor = "rgb(182, 250, 250)";
    }
  }
  else if (val === "ArrowUp"){
    if (activeY > 1){
      neighborColors(activeY.toString()+activeX.toString(), "white")
      activeY -= 1;
      activeCell = document.getElementById(activeY.toString()+activeX.toString())
      neighborColors(activeCell.id, "lightcyan")
      activeCell.style.backgroundColor = "rgb(182, 250, 250)";
    }
  }
  else if (val === "ArrowLeft"){
    if (activeX > 1){
      neighborColors(activeY.toString()+activeX.toString(), "white")
      activeX -= 1;
      activeCell = document.getElementById(activeY.toString()+activeX.toString())
      neighborColors(activeCell.id, "lightcyan")
      activeCell.style.backgroundColor = "rgb(182, 250, 250)";
    }
  }
  else if (val === "ArrowRight"){
    if (activeX < 9){
      neighborColors(activeY.toString()+activeX.toString(), "white")
      activeX += 1;
      activeCell = document.getElementById(activeY.toString()+activeX.toString())
      neighborColors(activeCell.id, "lightcyan")
      activeCell.style.backgroundColor = "rgb(182, 250, 250)";
    }
  }
}

function neighborColors(id, color){
  var y = Math.floor(id/10);
  var x = id % 10;
  for (let i = 1; i < 10; i++){
    var neighbor = document.getElementById((y*10+i).toString());
    neighbor.style.backgroundColor = color;
    neighbor = document.getElementById((i*10+x).toString());
    neighbor.style.backgroundColor = color;
  }
  var cornerY = Math.floor((y-1)/3)*3+1;
  var cornerX = Math.floor((x-1)/3)*3+1;
  for (let i = 0; i < 3; i++){
    for (let j = 0; j < 3; j++){
      var neighbor = document.getElementById(((cornerY+i)*10+cornerX+j).toString());
      neighbor.style.backgroundColor = color;
    }
  }
}

var togglePencil = document.createElement("button");
togglePencil.textContent = "Normal Mode";
togglePencil.style.borderColor = "rgb(194, 194, 194)";
togglePencil.onclick = function(){
  if (isPencil){
    togglePencil.textContent = "Normal Mode";
    togglePencil.style.borderColor = "rgb(194, 194, 194)";
  }
  else{
    togglePencil.textContent = "Pencil Mode";
    togglePencil.style.borderColor = "rgb(152, 3, 252)";
  }
  isPencil = !isPencil;
}
document.getElementById("buttonsContainer").appendChild(togglePencil);

var functions = document.createElement("div");
functions.setAttribute("id", "dropdownButton");
functions.textContent = "- - -";
functions.onclick = function(){
  if (dropdown.hasAttribute("hidden")){
    dropdown.removeAttribute("hidden");
  }
}
var dropdown = document.createElement("div");
dropdown.setAttribute("hidden", "hidden");
dropdown.setAttribute("id", "dropdownContainer");
var functionNames = ["Obvious", "Subsets", "X-Wing", "Swordfish", "Hidden Subsets"];
for (let i = 0; i < functionNames.length; i++){
  var choice = document.createElement("div");
  choice.textContent = functionNames[i];
  choice.setAttribute("class", "dropdown");
  choice.onclick = function(){
    functions.textContent = functionNames[i];
    dropdown.setAttribute("hidden", "hidden");
  }
  dropdown.appendChild(choice);
}
document.getElementById("buttonsContainer").appendChild(functions);
document.getElementById("buttonsContainer").appendChild(dropdown);

function highlightCell(idArr){
  for (let i = 0; i < idArr.length; i++){
    var cell = document.getElementById(idArr[i]);
    cell.style.backgroundColor = "rgb(255, 255, 204)";
  }
  setTimeout(function(){
    for (let i = 0; i < idArr.length; i++){
      var cell = document.getElementById(idArr[i]);
      if (cell === activeCell){
        cell.style.backgroundColor = "rgb(182, 250, 250)";
      }
      else if (Math.floor(idArr[i]/10)===Math.floor(activeCell.id/10) || idArr[i]%10===activeCell.id%10){
        cell.style.backgroundColor = "lightcyan";
      }
      else if (Math.floor((Math.floor(idArr[i]/10)-1)/3)===Math.floor((Math.floor(activeCell.id/10)-1)/3) && Math.floor((idArr[i]%10-1)/3) === Math.floor((activeCell.id%10-1)/3)){
        cell.style.backgroundColor = "lightcyan";
      }
      else{
        cell.style.backgroundColor = "white";
      }
    }
  }, 1000);
}

var test = document.createElement("button");
test.onclick = sendSudoku;
document.getElementById("buttonsContainer").appendChild(test);

async function sendSudoku() {
  var data = new FormData();
  for (let y=1; y<10; y++){
    for (let x=1; x<10; x++){
      var id = (y*10+x).toString();
      var value = document.getElementById("v"+id).innerHTML;
      if (value === ""){ // only send the pencils, not the final values
        for (let p=1; p<10; p++){
          var pencil = document.getElementById(id+p.toString());
          if (pencil.innerHTML !== ""){
            value += pencil.innerHTML;
          }
        }
        if (value !== ""){
          data.append(id.toString(), value.toString());
        }
      }
    }
  }
  data.append("function", functions.textContent);
  
  try {
    const response = await fetch('/submit_data', {
        method: 'POST',
        body: data
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    highlightCell(result.message);
  } 
  catch (error) {
    console.error('Error:', error);
  }
}