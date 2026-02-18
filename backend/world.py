import random
import re
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

    def add_log(self, message):
        """Добавляет сообщение в лог"""
        clean_message = re.sub(r'[^\x00-\x7Fа-яА-ЯёЁ\s\.,!?@-]', '', str(message))
        self.logs.append(clean_message)
        if len(self.logs) > 50:
            self.logs.pop(0)

    def tick(self):
        """Один шаг симуляции"""
        self.update_time()
        self.update_weather()

        # ✅ ВАЖНО: создаем список кроликов
        rabbits = list(self.agents.values())

        for rabbit in rabbits:
            rabbit.update()
            rabbit.move_randomly()

        for rabbit in rabbits:
            for other in rabbits:
                if other != rabbit:
                    reaction = rabbit.react_to_other_rabbit(other)
                    if reaction:
                        self.add_log(reaction)

        # случайный автономный диалог
        if random.random() < 0.25 and len(rabbits) >= 2:
            r1, r2 = random.sample(rabbits, 2)
            self.autonomous_dialogue(r1, r2)

        self.logs = self.logs[-20:]

    def autonomous_dialogue(self, r1, r2):
        """Диалог между персонажами"""
        context = {
            "time": self.time,
            "weather": self.weather
        }

        prompt = f"Поговори со мной о погоде или настроении"
        reply = r1.generate_response(prompt, context)
        self.add_log(reply)

        reply2 = r2.generate_response(reply, context)
        self.add_log(reply2)

    def update_time(self):
        self.time += 1
        if self.time >= 24:
            self.time = 0

    def update_weather(self):
        if random.random() < 0.15:
            self.weather = random.choice(["sunny", "rain", "cloudy"])

    def handle_user_message(self, message):
        message = message.strip()
        self.add_log(f"Ты: {message}")

        context = {
            "time": self.time,
            "weather": self.weather
        }

        if message.startswith("@"):
            parts = message.split(" ", 1)
            target_name = parts[0][1:]
            text = parts[1] if len(parts) > 1 else ""

            if target_name in self.agents:
                reply = self.agents[target_name].generate_response(text, context)
                self.add_log(reply)
        else:
            for rabbit in self.agents.values():
                reply = rabbit.generate_response(message, context)
                self.add_log(reply)

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