let rows = 6;
let cols = 6;

let agentPos = {x: 0, y: 0};
let steps = 0;

function createGrid() {
  let grid = document.getElementById("grid");
  grid.innerHTML = "";

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      let cell = document.createElement("div");
      cell.className = "cell";
      cell.id = `cell-${i}-${j}`;
      grid.appendChild(cell);
    }
  }
}

function step() {
  steps++;
  document.getElementById("steps").innerText = steps;

  // simulate percepts
  let percepts = ["Breeze", "Stench"][Math.floor(Math.random()*2)];
  document.getElementById("percepts").innerText = percepts;

  let cell = document.getElementById(`cell-${agentPos.x}-${agentPos.y}`);
  cell.classList.add("safe");

  agentPos.x = (agentPos.x + 1) % rows;
}

createGrid();