"""
Главный сервер AI Rabbit World
Flask + SocketIO (без eventlet)
"""

# ========== ИСПРАВЛЕНИЕ КОДИРОВКИ ==========
import sys
import io

# Устанавливаем UTF-8 для консоли Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# ============================================

from flask import Flask, render_template
from flask_socketio import SocketIO
import time

from world import World

# ================================
# ИНИЦИАЛИЗАЦИЯ
# ================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Добавляем секретный ключ
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
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
    try:
        text = data.get("text", "")
        if text:  # Проверяем, что сообщение не пустое
            world.handle_user_message(text)
            socketio.emit("world_update", world.get_state())
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")


@socketio.on("connect")
def handle_connect():
    """При подключении клиента отправляем текущее состояние"""
    print("Клиент подключился")
    socketio.emit("world_update", world.get_state())


@socketio.on("disconnect")
def handle_disconnect():
    print("Клиент отключился")


# ================================
# GAME LOOP
# ================================

def game_loop():
    """
    Основной цикл симуляции
    """
    print(" Запуск игрового цикла...")
    while True:
        try:
            world.tick()
            socketio.emit("world_update", world.get_state())
            time.sleep(2)  # Пауза 2 секунды между тиками
        except Exception as e:
            print(f"Ошибка в игровом цикле: {e}")
            time.sleep(1)  # Пауза при ошибке


# ================================
# START
# ================================

if __name__ == "__main__":
    print("=" * 50)
    print("AI Rabbit World запускается...")
    print(f" Мир создан с {len(world.agents)} кроликами")
    print("=" * 50)

    # Запускаем игровой цикл в фоне
    socketio.start_background_task(game_loop)

    # Запускаем сервер (ТОЛЬКО ОДИН РАЗ!)
    socketio.run(app,
                 host='127.0.0.1',
                 port=8050,
                 debug=True,
                 allow_unsafe_werkzeug=True)