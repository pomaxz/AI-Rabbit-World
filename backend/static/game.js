const socket = io();

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth - 320;
canvas.height = window.innerHeight - 60;

let world = null;

socket.on("world_update", (data) => {
    world = data;
    updateHUD();
    updateCharacters();
    updateChat();
});

function updateHUD() {
    document.getElementById("timeTracker").innerText =
        "🕒 Время: " + world.time + ":00";

    document.getElementById("weatherTracker").innerText =
        "🌦 Погода: " + world.weather;
}

function updateChat() {
    const chat = document.getElementById("chat");
    chat.innerHTML = "";

    world.logs.forEach(msg => {
        const div = document.createElement("div");
        div.className = "chat-message";
        div.innerText = msg;
        chat.appendChild(div);
    });
}

function updateCharacters() {
    const container = document.getElementById("characters");
    container.innerHTML = "";

    Object.entries(world.agents).forEach(([name, rabbit]) => {

        let mood =
            (rabbit.needs.energy +
             rabbit.needs.hunger +
             rabbit.needs.social) / 3;

        const card = document.createElement("div");
        card.className = "character-card";

        const moodBar = document.createElement("div");
        moodBar.className = "mood-bar";

        const moodFill = document.createElement("div");
        moodFill.className = "mood-fill";
        moodFill.style.width = mood + "%";

        if (mood > 70) moodFill.style.background = "#22c55e";
        else if (mood > 40) moodFill.style.background = "#facc15";
        else moodFill.style.background = "#ef4444";

        moodBar.appendChild(moodFill);

        card.innerHTML = `<strong>${name}</strong>`;
        card.appendChild(moodBar);

        container.appendChild(card);
    });
}

function drawBackground(time) {
    let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);

    if (time >= 6 && time < 18) {
        gradient.addColorStop(0, "#87CEEB");
        gradient.addColorStop(1, "#4CAF50");
    } else {
        gradient.addColorStop(0, "#0f172a");
        gradient.addColorStop(1, "#111827");
    }

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawRabbit(name, rabbit) {
    ctx.font = "28px Arial";
    ctx.fillText("🐰", rabbit.x, rabbit.y);

    if (rabbit.last_message) {
        ctx.fillStyle = "white";
        ctx.fillRect(rabbit.x, rabbit.y - 35, 120, 25);

        ctx.fillStyle = "black";
        ctx.font = "11px Arial";
        ctx.fillText(rabbit.last_message,
                     rabbit.x + 5,
                     rabbit.y - 18);
    }
}

function render() {
    if (!world) return;

    drawBackground(world.time);

    Object.entries(world.agents).forEach(([name, rabbit]) => {
        drawRabbit(name, rabbit);
    });
}

function gameLoop() {
    render();
    requestAnimationFrame(gameLoop);
}

const input = document.createElement("input");
input.placeholder = "@Luna привет или всем привет";
input.style.position = "absolute";
input.style.bottom = "20px";
input.style.left = "20px";
input.style.width = "300px";
input.style.padding = "8px";
document.body.appendChild(input);

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        socket.emit("user_message", { text: input.value });
        input.value = "";
    }
});


gameLoop();
