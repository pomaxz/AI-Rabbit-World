"""
Главный сервер AI Rabbit World
Flask + SocketIO (без eventlet)
"""

from flask import Flask, render_template
from flask_socketio import SocketIO
import time

from world import World

# ================================
# ИНИЦИАЛИЗАЦИЯ
# ================================

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
world = World()

# ================================
# ROUTES
# ================================

@app.route("/")
def index():
    return render_template("index.html")

# ================================
# SOCKET EVENTS
# ================================

@socketio.on("user_message")
def handle_user_message(data):
    """
    Получение сообщения от пользователя
    """
    text = data.get("text", "")
    world.handle_user_message(text)

    # Отправляем обновление всем клиентам
    socketio.emit("world_update", world.get_state())

# ================================
# GAME LOOP
# ================================

def game_loop():
    """
    Основной цикл симуляции
    """
    while True:
        world.tick()
        socketio.emit("world_update", world.get_state())
        time.sleep(2)

# ================================
# START
# ================================

if __name__ == "__main__":
    socketio.start_background_task(game_loop)
    socketio.run(app, port=8050, debug=True)


if __name__ == "__main__":
    socketio.start_background_task(game_loop)
    socketio.run(app, port=8050, debug=True)
