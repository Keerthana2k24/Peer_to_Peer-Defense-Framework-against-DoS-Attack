const API = "http://127.0.0.1:8000/nodes";
const nodesDiv = document.getElementById("nodes");
const svg = document.getElementById("links");

const open = new Set();

function drawLinks(coords) {
    svg.innerHTML = "";
    const ids = Object.keys(coords);

    for (let i = 0; i < ids.length; i++) {
        for (let j = i + 1; j < ids.length; j++) {
            const a = coords[ids[i]];
            const b = coords[ids[j]];

            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", a.x);
            line.setAttribute("y1", a.y);
            line.setAttribute("x2", b.x);
            line.setAttribute("y2", b.y);
            line.setAttribute("stroke", "rgba(255,255,255,0.2)");
            svg.appendChild(line);
        }
    }
}

async function refresh() {
    const res = await fetch(API);
    const data = await res.json();

    nodesDiv.innerHTML = "";
    svg.innerHTML = "";

    const keys = Object.keys(data);
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    const r = 220;

    const coords = {};

    keys.forEach((id, i) => {
        const angle = (2 * Math.PI / keys.length) * i;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);

        coords[id] = { x, y };

        const node = document.createElement("div");
        node.className = "node";
        node.style.left = `${x - 80}px`;
        node.style.top = `${y - 50}px`;

        if (open.has(id)) node.classList.add("active");

        node.innerHTML = `
            <b>${id}</b>
            <div class="status ${data[id].status}">${data[id].status}</div>
            <div class="details">
                <div>Port: ${data[id].port}</div>
                <div>${data[id].prediction}</div>
            </div>
        `;

        node.onclick = () => {
            open.has(id) ? open.delete(id) : open.add(id);
            node.classList.toggle("active");
        };

        nodesDiv.appendChild(node);
    });

    drawLinks(coords);
}

setInterval(refresh, 1000);
refresh();
