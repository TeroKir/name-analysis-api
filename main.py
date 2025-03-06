import re
import json
import random
import pandas as pd
from collections import Counter
from fastapi import FastAPI, HTTPException
import uvicorn
import logging
from cachetools import TTLCache
from supabase import create_client, Client

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Подключение к Supabase (замени URL и API-ключ на свои)
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-supabase-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Загрузка базы данных (руны, Таро, нумерология, астрология, психология)
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# Кэш для ускорения повторных запросов (1 час хранения данных)
cache = TTLCache(maxsize=1000, ttl=3600)

# Инициализация FastAPI
app = FastAPI()

# Функция перевода имени в рунический код
def name_to_runes(name):
    return [DATA["runes"].get(letter.upper(), "-") for letter in name if letter.upper() in DATA["runes"]]

# Функция перевода имени в Таро-архетипы
def name_to_tarot(name):
    tarot_numbers = [(ord(letter.upper()) - 65) % 22 for letter in name if letter.isalpha()]
    tarot_cards = [DATA["tarot"].get(str(num), "Unknown") for num in tarot_numbers]
    return list(set(tarot_cards))  # Исключаем дублирование

# Функция перевода имени в числовой код (гематрия)
def name_to_numerology(name):
    numbers = [(ord(letter.upper()) - 64) % 9 + 1 for letter in name if letter.isalpha()]
    total = sum(numbers) % 9 + 1
    return total, DATA["numerology"].get(str(total), "No Data")

# Функция перевода имени в астрологический код
def name_to_astrology(name):
    planets = [DATA["planets"].get(letter.upper(), "Unknown") for letter in name if letter.upper() in DATA["planets"]]
    most_common_planet = Counter(planets).most_common(1)
    dominant_planet = most_common_planet[0][0] if most_common_planet else "Unknown"
    return dominant_planet, DATA["astrology"].get(dominant_planet, "No Data")

# Генерация психологического анализа (архетипы Юнга + Big Five)
def generate_psychology_analysis(name):
    name_hash = sum(ord(c) for c in name) % len(DATA["psychology"])
    return DATA["psychology"][name_hash]

# Основная функция анализа имени
def analyze_name(name):
    name = re.sub(r'[^a-zA-Zа-яА-Я]', '', name).strip()  # Убираем лишние символы и пробелы
    if not name:
        raise HTTPException(status_code=400, detail="Имя не должно быть пустым")

    # Проверяем кэш
    if name in cache:
        logging.info(f"Кэшированное значение найдено для {name}")
        return cache[name]

    # Проверяем базу данных Supabase
    existing_entry = supabase.table("users_analysis").select("*").eq("name", name).execute()
    if existing_entry.data:
        result = json.loads(existing_entry.data[0]["result"])
        cache[name] = result  # Сохраняем в кэше
        return result

    # Генерируем новый анализ
    runes = name_to_runes(name)
    tarot = name_to_tarot(name)
    numerology, numerology_meaning = name_to_numerology(name)
    astrology, astrology_description = name_to_astrology(name)
    psychology = generate_psychology_analysis(name)

    result = {
        "Имя": name,
        "Рунический анализ": runes,
        "Таро-архетипы": tarot,
        "Нумерология": {"Число": numerology, "Значение": numerology_meaning},
        "Астрология": {"Планета": astrology, "Описание": astrology_description},
        "Психологический профиль": psychology
    }

    # Сохраняем в базу данных и кэш
    supabase.table("users_analysis").insert({"name": name, "result": json.dumps(result)}).execute()
    cache[name] = result

    return result

@app.get("/analyze/{name}")
def analyze_name_api(name: str):
    return analyze_name(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
