let rows = 6;
let cols = 6;

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

async function step() {
  const res = await fetch("http://127.0.0.1:5000/step");
  const data = await res.json();

  document.querySelectorAll(".cell").forEach(cell => {
    cell.className = "cell unknown";
    cell.innerHTML = "";
  });

  data.safe.forEach(([x, y]) => {
    document.getElementById(`cell-${x}-${y}`).classList.add("safe");
  });

  data.danger.forEach(([x, y]) => {
    document.getElementById(`cell-${x}-${y}`).classList.add("danger");
  });

  data.visited.forEach(([x, y]) => {
    let cell = document.getElementById(`cell-${x}-${y}`);
    cell.classList.add("safe");
  });

  let agentCell = document.getElementById(`cell-${data.x}-${data.y}`);
  agentCell.classList.add("agent");

  agentCell.innerHTML = `<div class="percept">${data.percepts.join("<br>")}</div>`;

  document.getElementById("percepts").innerText = data.percepts.join(", ");
  document.getElementById("steps").innerText = data.steps;

  let log = document.getElementById("log");
  log.innerHTML += `<p>Moved to (${data.x}, ${data.y}) → ${data.percepts.join(", ") || "No percepts"}</p>`;
}

async function reset() {
  await fetch("http://127.0.0.1:5000/reset");
  createGrid();
}

createGrid();