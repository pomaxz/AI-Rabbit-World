import os
import random
from groq import Groq

# ВСТАВЬТЕ СВОЙ КЛЮЧ GROQ ЗДЕСЬ
GROQ_API_KEY = "gsk_ваш_ключ_сюда"  # Замените на ваш реальный ключ

# Инициализируем клиент Groq
if GROQ_API_KEY and GROQ_API_KEY != "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":
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None
class Rabbit:
    def __init__(self, name, personality):
        self.name = name
        self.personality = personality
        self.x = random.randint(200, 400)  # Случайная начальная позиция
        self.y = random.randint(200, 400)
        self.needs = {
            "energy": random.randint(70, 100),
            "hunger": random.randint(70, 100),
            "social": random.randint(70, 100)
        }
        self.mood = 100
        self.memory = []
        self.last_message = ""

        # Новые атрибуты для живости
        self.age = random.randint(1, 5)
        self.favorite_food = random.choice(["морковка", "клевер", "яблоко", "одуванчики", "капуста"])
        self.hobbies = random.choice(["прыгать", "копать норки", "играть", "спать", "наблюдать", "петь"])
        self.friends = []
        self.enemies = []
        self.daily_goal = random.choice(["найти еду", "погулять", "поспать", "познакомиться", "поиграть", "исследовать"])
        self.energy_level = random.choice(["бодрый", "уставший", "сонный", "активный", "игривый"])
        self.speak_style = random.choice(["быстро", "медленно", "весело", "задумчиво", "застенчиво", "громко"])
        self.last_interaction = None
        self.interaction_count = 0

    def update(self):
        # Обновляем настроение
        self.mood = sum(self.needs.values()) / 3

        # Естественное изменение потребностей
        self.needs["energy"] = max(0, self.needs["energy"] - random.uniform(0.1, 0.5))
        self.needs["hunger"] = max(0, self.needs["hunger"] - random.uniform(0.2, 0.6))
        self.needs["social"] = max(0, self.needs["social"] - random.uniform(0.1, 0.4))

        # Случайные изменения настроения
        if random.random() < 0.1:  # 10% шанс
            self.mood += random.randint(-5, 5)
            self.mood = max(0, min(100, self.mood))

        # Если социальная потребность низкая - ищем друзей
        if self.needs["social"] < 30 and random.random() < 0.2:
            self.daily_goal = "найти друзей"

    def move_randomly(self):
        """Случайное движение кролика"""
        if random.random() < 0.3:  # 30% шанс двигаться
            # Движение зависит от энергии
            if self.needs["energy"] > 50:
                step = random.randint(-15, 15)
            else:
                step = random.randint(-5, 5)

            self.x += step
            self.y += step

            # Ограничиваем движение в пределах экрана
            self.x = max(50, min(750, self.x))
            self.y = max(50, min(550, self.y))
            return True
        return False

    def react_to_other_rabbit(self, other_rabbit):
        """Реакция на другого кролика"""
        # Вычисляем расстояние
        distance = ((self.x - other_rabbit.x) ** 2 + (self.y - other_rabbit.y) ** 2) ** 0.5

        if distance < 60:  # Если близко
            self.interaction_count += 1

            if other_rabbit.name in self.friends:
                if random.random() < 0.3:
                    return f"{self.name} обнимает {other_rabbit.name}! 🤗"
                else:
                    return f"{self.name} радостно прыгает вокруг {other_rabbit.name} 🐰"

            elif other_rabbit.name in self.enemies:
                self.x += 30  # Убегает подальше
                return f"{self.name} недовольно фыркает и убегает от {other_rabbit.name} 😤"

            else:
                # Случайно может стать другом или врагом
                if random.random() < 0.2:  # 20% шанс подружиться
                    self.friends.append(other_rabbit.name)
                    self.needs["social"] = min(100, self.needs["social"] + 20)
                    return f"{self.name} подружился с {other_rabbit.name}! 🎉"
                elif random.random() < 0.1:  # 10% шанс стать врагом
                    self.enemies.append(other_rabbit.name)
                    return f"{self.name} поссорился с {other_rabbit.name}! 😠"
        return None

    def generate_response(self, user_text, world_context):
        """Генерирует ответ кролика"""

        # Если есть API ключ, пробуем использовать Groq
        if client:
            try:
                # Добавляем контекст о личности
                personality_extra = f"""
Ты {self.energy_level} кролик.
Ты говоришь {self.speak_style}.
Твоя любимая еда: {self.favorite_food}.
Твое хобби: {self.hobbies}.
Сегодня ты хочешь: {self.daily_goal}.
"""

                system_prompt = f"""
Ты — кролик по имени {self.name}.
Твоя личность: {self.personality}.
{personality_extra}
Текущее настроение: {self.mood:.1f}/100.
Погода: {world_context.get('weather', 'ясно')}.
Время суток: {world_context.get('time', 'день')}.

Отвечай как живой персонаж со своим характером.
Будь естественным, эмоциональным.
Используй иногда междометия (Ой! Ах! Ух ты!).
Можешь упоминать свои желания и чувства.
Не упоминай что ты ИИ.
Говори кратко (1-3 предложения).
"""

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]

                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=messages,
                    temperature=0.8,
                    max_tokens=100
                )
                reply = response.choices[0].message.content

            except Exception as e:
                print(f"Ошибка API: {e}")
                reply = self._get_local_response(user_text)
        else:
            # Используем локальные ответы
            reply = self._get_local_response(user_text)

        self.last_message = reply
        self.memory.append({"user": user_text, "reply": reply})

        # Социальная потребность растет когда общаются
        self.needs["social"] = min(100, self.needs["social"] + 5)

        return f"{self.name}: {reply}"

    def _get_local_response(self, user_text):
        """Локальные ответы без API"""

        # Анализируем текст сообщения
        user_text_lower = user_text.lower()

        # Ответы в зависимости от контекста
        if "привет" in user_text_lower or "здравствуй" in user_text_lower:
            responses = [
                f"Привет! Я {self.name}! Рад тебя видеть! 🐰",
                f"Ой, здравствуй! Как дела?",
                f"Привет-привет! Хочешь поиграть?"
            ]
        elif "как дела" in user_text_lower:
            responses = [
                f"У меня всё отлично! Настроение {self.mood:.0f} из 100!",
                f"Хорошо! Сегодня я {self.energy_level} и хочу {self.daily_goal}",
                f"Неплохо! Вот только {self.favorite_food} съел бы..."
            ]
        elif "погода" in user_text_lower:
            responses = [
                f"Сегодня отличная погода для {self.hobbies}!",
                f"Люблю такую погоду, можно {self.hobbies}",
                f"Хорошо, что не дождь! А то мои ушки промокнут"
            ]
        elif "пойдем" in user_text_lower or "гулять" in user_text_lower:
            responses = [
                f"С удовольствием! Я как раз хотел {self.daily_goal}!",
                f"Ура! Пойдем! Я покажу тебе полянку с {self.favorite_food}",
                f"Давай! Только догони меня!"
            ]
        elif "морковк" in user_text_lower or self.favorite_food in user_text_lower:
            responses = [
                f"Ммм, {self.favorite_food}! Моя любимая еда!",
                f"А ты знаешь, что кролики обожают {self.favorite_food}?",
                f"Самый вкусный {self.favorite_food} - тот, что найдешь сам!"
            ]
        elif "пока" in user_text_lower or "до свидания" in user_text_lower:
            responses = [
                f"Пока! Заходи еще!",
                f"До встречи! Буду скучать!",
                f"Пока-пока! Увидимся позже!"
            ]
        else:
            # Случайные фразы
            responses = [
                f"{self.name} {self.hobbies} и довольно улыбается 😊",
                f"*грызет {self.favorite_food} с аппетитом*",
                f"Сегодня я {self.energy_level} и хочу {self.daily_goal}",
                f"{self.name} внимательно слушает и кивает",
                f"Ой! А что это там? *прислушивается*",
                f"*шевелит длинными ушками*",
                f"Хороший денек, чтобы {self.hobbies}!",
                f"Мне нравится с тобой разговаривать!"
            ]

        return random.choice(responses)

    def __str__(self):
        friends_list = ", ".join(self.friends) if self.friends else "нет друзей"
        return f"{self.name} ({self.personality}) - {self.energy_level}, любит {self.favorite_food}, друзья: {friends_list}"