import os
from dotenv import load_dotenv
from groq import Groq

# Загружаем .env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))



class Rabbit:
    def __init__(self, name, personality):
        self.name = name
        self.personality = personality

        self.x = 300
        self.y = 300

        self.needs = {
            "energy": 100,
            "hunger": 100,
            "social": 100,
        }

        self.mood = 100
        self.memory = []
        self.last_message = ""

    # =============================

    def update(self):
        self.mood = sum(self.needs.values()) / 3

    # =============================
    # LLM ОТВЕТ
    # =============================

    def generate_response(self, user_text, world_context):

        system_prompt = f"""
Ты — кролик по имени {self.name}.
Твоя личность: {self.personality}.
Текущее настроение: {self.mood}.
Погода: {world_context['weather']}.
Время суток: {world_context['time']}.

Отвечай как живой персонаж.
Будь естественным.
Не упоминай что ты ИИ.
Говори кратко (1-3 предложения).
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content

        self.last_message = reply
        self.memory.append({"user": user_text, "reply": reply})

        return f"{self.name}: {reply}"
