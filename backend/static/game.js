const socket = io();

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth - 320;
canvas.height = window.innerHeight - 60;

let world = null;
let particles = []; // Для эффектов дождя/снега

socket.on("world_update", (data) => {
    world = data;
    updateHUD();
    updateCharacters();
    updateChat();

    // Создаем эффекты в зависимости от погоды
    createWeatherEffects(world.weather);
});

// ========== НОВЫЕ ФУНКЦИИ ДЛЯ ПОГОДЫ ==========

function createWeatherEffects(weather) {
    particles = [];

    if (weather === 'rain') {
        // Создаем капли дождя
        for (let i = 0; i < 100; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                speed: 5 + Math.random() * 5,
                length: 15 + Math.random() * 10
            });
        }
    } else if (weather === 'cloudy') {
        // Создаем облака
        for (let i = 0; i < 3; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: 50 + Math.random() * 200,
                size: 50 + Math.random() * 50,
                speed: 0.2 + Math.random() * 0.3
            });
        }
    }
}

function drawWeatherEffects() {
    if (!world) return;

    if (world.weather === 'rain') {
        // Рисуем дождь
        ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
        ctx.lineWidth = 1.5;

        particles.forEach(p => {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x - 3, p.y + p.length);
            ctx.strokeStyle = "rgba(174, 194, 224, 0.6)";
            ctx.stroke();

            // Движение дождя
            p.y += p.speed;
            if (p.y > canvas.height) {
                p.y = 0;
                p.x = Math.random() * canvas.width;
            }
        });
    }

    if (world.weather === 'cloudy') {
        // Рисуем облака
        particles.forEach(p => {
            ctx.fillStyle = "rgba(255, 255, 255, 0.4)";

            // Рисуем пушистое облако
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size * 0.3, 0, Math.PI * 2);
            ctx.arc(p.x + 30, p.y - 10, p.size * 0.25, 0, Math.PI * 2);
            ctx.arc(p.x - 20, p.y - 5, p.size * 0.25, 0, Math.PI * 2);
            ctx.arc(p.x + 10, p.y + 10, p.size * 0.2, 0, Math.PI * 2);
            ctx.fill();

            // Движение облаков
            p.x += p.speed;
            if (p.x > canvas.width + 100) {
                p.x = -100;
                p.y = 50 + Math.random() * 200;
            }
        });
    }

    if (world.weather === 'sunny') {
        // Рисуем солнечные лучи
        const time = Date.now() / 1000;

        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2 + time * 0.5;
            const x = canvas.width - 80 + Math.cos(angle) * 50;
            const y = 80 + Math.sin(angle) * 50;

            ctx.beginPath();
            ctx.moveTo(canvas.width - 80, 80);
            ctx.lineTo(x, y);
            ctx.strokeStyle = "rgba(255, 215, 0, 0.3)";
            ctx.lineWidth = 2;
            ctx.stroke();
        }

        // Солнце
        ctx.beginPath();
        ctx.arc(canvas.width - 80, 80, 35, 0, Math.PI * 2);
        ctx.fillStyle = "#ffd700";
        ctx.shadowColor = "#ffd700";
        ctx.shadowBlur = 30;
        ctx.fill();
        ctx.shadowBlur = 0;
    }
}

// ========== ОСНОВНЫЕ ФУНКЦИИ ==========

function updateHUD() {
    document.getElementById("timeTracker").innerText =
        "🕒 Время: " + world.time + ":00";

    // Иконки для погоды
    let weatherIcon = "☀️";
    if (world.weather === 'rain') weatherIcon = "🌧️";
    if (world.weather === 'cloudy') weatherIcon = "☁️";

    document.getElementById("weatherTracker").innerHTML =
        `🌦 Погода: ${world.weather} ${weatherIcon}`;
}

function updateChat() {
    const chat = document.getElementById("chat");
    chat.innerHTML = "";

    // Показываем только последние 10 сообщений
    world.logs.slice(-10).forEach(msg => {
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

function drawBackground(time, weather) {
    let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);

    if (time >= 6 && time < 18) {
        // ДНЕВНОЙ ФОН
        if (weather === 'sunny') {
            gradient.addColorStop(0, "#87CEEB");  // Голубое небо
            gradient.addColorStop(0.6, "#90EE90"); // Зеленая трава
            gradient.addColorStop(1, "#4CAF50");   // Темно-зеленая трава
        }
        else if (weather === 'cloudy') {
            gradient.addColorStop(0, "#B0C4DE");  // Серо-голубое небо
            gradient.addColorStop(0.6, "#6B8E23"); // Оливковая трава
            gradient.addColorStop(1, "#556B2F");   // Темно-оливковая
        }
        else if (weather === 'rain') {
            gradient.addColorStop(0, "#4682B4");  // Стальное небо
            gradient.addColorStop(0.6, "#2E4A2E"); // Темно-зеленая трава
            gradient.addColorStop(1, "#1A2F1A");   // Очень темная трава
        }
        else {
            gradient.addColorStop(0, "#87CEEB");
            gradient.addColorStop(1, "#4CAF50");
        }
    } else {
        // НОЧНОЙ ФОН
        if (weather === 'sunny') {
            gradient.addColorStop(0, "#0A192F");  // Темно-синее небо
            gradient.addColorStop(0.6, "#1A2F1A"); // Темная трава
            gradient.addColorStop(1, "#0A1F0A");   // Черная трава

            // Рисуем луну
            ctx.shadowColor = "#fff";
            ctx.shadowBlur = 20;
            ctx.beginPath();
            ctx.arc(canvas.width - 80, 80, 25, 0, Math.PI * 2);
            ctx.fillStyle = "#F8F8FF";
            ctx.fill();

            // Рисуем звезды
            for (let i = 0; i < 20; i++) {
                if (Math.random() > 0.5) {
                    ctx.beginPath();
                    ctx.arc(100 + i * 30, 50 + (i % 5) * 30, 1 + Math.random() * 2, 0, Math.PI * 2);
                    ctx.fillStyle = "#fff";
                    ctx.fill();
                }
            }
            ctx.shadowBlur = 0;
        }
        else if (weather === 'cloudy') {
            gradient.addColorStop(0, "#1A1F2E");  // Темно-серое небо
            gradient.addColorStop(0.6, "#0F1F0F"); // Темная трава
            gradient.addColorStop(1, "#0A1F0A");   // Черная трава
        }
        else if (weather === 'rain') {
            gradient.addColorStop(0, "#0A0F1A");  // Черно-синее небо
            gradient.addColorStop(0.6, "#0A1F0A"); // Черная трава
            gradient.addColorStop(1, "#051205");   // Совсем черная
        }
        else {
            gradient.addColorStop(0, "#0f172a");
            gradient.addColorStop(1, "#111827");
        }
    }

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Рисуем травинки
    ctx.fillStyle = "rgba(0, 100, 0, 0.3)";
    for (let i = 0; i < 50; i++) {
        let x = i * 20 + Math.random() * 10;
        let height = 20 + Math.random() * 30;
        ctx.fillRect(x, canvas.height - height, 2, height);
    }
}

function drawRabbit(name, rabbit) {
    // Эмодзи кролика
    ctx.font = "36px Arial";
    ctx.fillText("🐰", rabbit.x - 15, rabbit.y - 10);

    // Имя над кроликом
    ctx.font = "bold 14px Arial";
    ctx.fillStyle = "white";
    ctx.shadowColor = "black";
    ctx.shadowBlur = 4;
    ctx.fillText(name, rabbit.x - 20, rabbit.y - 40);
    ctx.shadowBlur = 0;

    // Облачко с сообщением
    if (rabbit.last_message) {
        ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
        ctx.shadowBlur = 10;
        ctx.shadowColor = "rgba(0,0,0,0.3)";

        // Измеряем текст
        ctx.font = "12px Arial";
        let textWidth = ctx.measureText(rabbit.last_message).width;
        let boxWidth = Math.min(200, textWidth + 20);

        // Рисуем облачко
        ctx.beginPath();
        ctx.roundRect(rabbit.x - 20, rabbit.y - 80, boxWidth, 30, 10);
        ctx.fill();

        ctx.fillStyle = "#333";
        ctx.font = "12px Arial";
        ctx.fillText(rabbit.last_message, rabbit.x - 15, rabbit.y - 60);
        ctx.shadowBlur = 0;
    }
}

// Вспомогательная функция для скругленных прямоугольников
CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    this.moveTo(x + r, y);
    this.lineTo(x + w - r, y);
    this.quadraticCurveTo(x + w, y, x + w, y + r);
    this.lineTo(x + w, y + h - r);
    this.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    this.lineTo(x + r, y + h);
    this.quadraticCurveTo(x, y + h, x, y + h - r);
    this.lineTo(x, y + r);
    this.quadraticCurveTo(x, y, x + r, y);
    this.closePath();
    return this;
};

function render() {
    if (!world) return;

    drawBackground(world.time, world.weather);
    drawWeatherEffects();

    Object.entries(world.agents).forEach(([name, rabbit]) => {
        drawRabbit(name, rabbit);
    });
}

function gameLoop() {
    render();
    requestAnimationFrame(gameLoop);
}

// Стилизованный input
const input = document.createElement("input");
input.placeholder = "💬 @Luna привет или всем привет";
input.style.position = "fixed";
input.style.bottom = "30px";
input.style.left = "50%";
input.style.transform = "translateX(-50%)";
input.style.width = "400px";
input.style.padding = "15px 25px";
input.style.border = "2px solid #4a90e2";
input.style.borderRadius = "50px";
input.style.fontSize = "16px";
input.style.backgroundColor = "rgba(255,255,255,0.95)";
input.style.boxShadow = "0 10px 30px rgba(0,0,0,0.3)";
input.style.zIndex = "1000";
document.body.appendChild(input);

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        socket.emit("user_message", { text: input.value });
        input.value = "";
    }
});

gameLoop();