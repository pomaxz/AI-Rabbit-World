import random
from agents import Rabbit


class World:
    def __init__(self):
        self.time = 8
        self.weather = "sunny"
        self.logs = []

        self.agents = {
            "Luna": Rabbit("Luna", "мечтательная и эмоциональная"),
            "Max": Rabbit("Max", "энергичный и прямолинейный"),
            "Ruby": Rabbit("Ruby", "спокойная и рассудительная"),
        }

    # =====================================================

    def tick(self):
        """Один шаг симуляции"""

        self.update_time()
        self.update_weather()

        rabbits = list(self.agents.values())

        # обновляем состояние
        for rabbit in rabbits:
            rabbit.update()

        # случайный автономный диалог (реже, чтобы не спамило)
        if random.random() < 0.25:
            r1, r2 = random.sample(rabbits, 2)
            self.autonomous_dialogue(r1, r2)

        self.logs = self.logs[-20:]

    # =====================================================

    def autonomous_dialogue(self, r1, r2):
        """Диалог между персонажами через LLM"""

        context = {
            "time": self.time,
            "weather": self.weather
        }

        prompt = f"""
Ты — {r1.name}.
Ты общаешься с {r2.name}.
Погода: {self.weather}.
Время: {self.time}.
Твоё настроение: {r1.mood}.

Скажи одну короткую естественную реплику.
"""

        reply = r1.generate_response(prompt, context)
        self.logs.append(reply)

    # =====================================================

    def update_time(self):
        self.time += 1
        if self.time >= 24:
            self.time = 0

    def update_weather(self):
        if random.random() < 0.15:
            self.weather = random.choice(["sunny", "rain", "cloudy"])

    # =====================================================
    # Пользовательский чат
    # =====================================================

    def handle_user_message(self, message):

        message = message.strip()
        self.logs.append(f"👤 Ты: {message}")

        context = {
            "time": self.time,
            "weather": self.weather
        }

        # Личное обращение
        if message.startswith("@"):
            parts = message.split(" ", 1)
            target_name = parts[0][1:]
            text = parts[1] if len(parts) > 1 else ""

            if target_name in self.agents:
                reply = self.agents[target_name].generate_response(
                    text,
                    context
                )
                self.logs.append(reply)

        # Общее сообщение
        else:
            for rabbit in self.agents.values():
                reply = rabbit.generate_response(message, context)
                self.logs.append(reply)

    # =====================================================

    def get_state(self):
        return {
            "time": self.time,
            "weather": self.weather,
            "logs": self.logs,
            "agents": {
                name: {
                    "x": r.x,
                    "y": r.y,
                    "needs": r.needs,
                    "mood": r.mood,
                    "last_message": r.last_message,
                }
                for name, r in self.agents.items()
            }
        }
