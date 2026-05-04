let rows = 6;
let cols = 6;
let perceptMap = {};

const API_BASE = "https://wumpus-agent-production-cb9a.up.railway.app";

function createGrid() {
    let grid = document.getElementById("grid");
    grid.innerHTML = "";

    grid.style.gridTemplateColumns = `repeat(${cols}, 60px)`;

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            let cell = document.createElement("div");
            cell.className = "cell unknown";
            cell.id = `cell-${i}-${j}`;
            grid.appendChild(cell);
        }
    }
}

async function step() {
    const res = await fetch(`${API_BASE}/step`);
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

    perceptMap[`${data.x}-${data.y}`] = data.percepts;

    document.getElementById("percepts").innerText =
        data.percepts.length ? data.percepts.join(", ") : "None";

    document.getElementById("steps").innerText = data.steps;

    let log = document.getElementById("log");
    log.innerHTML += `<p>Moved to (${data.x}, ${data.y}) → ${data.percepts.join(", ") || "No percepts"}</p>`;

    if (log.children.length > 20) {
        log.removeChild(log.firstChild);
    }

    for (let key in perceptMap) {
        let [x, y] = key.split("-").map(Number);
        let cell = document.getElementById(`cell-${x}-${y}`);
        let percepts = perceptMap[key];

        let html = percepts.map(p => {
            if (p === "Breeze") return `<span class="tag breeze">B</span>`;
            if (p === "Stench") return `<span class="tag stench">S</span>`;
            return "";
        }).join("");

        if (cell.classList.contains("agent")) {
            cell.innerHTML = `
                <div class="agent-icon">A</div>
                <div class="percepts">${html}</div>
            `;
        } else {
            cell.innerHTML = `<div class="percepts">${html}</div>`;
        }
    }
}

async function reset() {
    rows = parseInt(document.getElementById("rows").value);
    cols = parseInt(document.getElementById("cols").value);

    await fetch(`${API_BASE}/reset?rows=${rows}&cols=${cols}`);

    perceptMap = {};
    createGrid();
}

createGrid();