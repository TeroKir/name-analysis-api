import json
from collections import Counter

# Load data from JSON
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# Convert name to runic symbols
def name_to_runes(name):
    return [DATA["runes"].get(letter.upper(), "-") for letter in name if letter.upper() in DATA["runes"]]

# Convert name to Tarot archetypes
def name_to_tarot(name):
    tarot_numbers = [(ord(letter.upper()) - 65) % 22 for letter in name if letter.isalpha()]
    tarot_cards = [DATA["tarot"].get(str(num), "Unknown") for num in tarot_numbers]
    return list(set(tarot_cards))  # Remove duplicates

# Convert name to numerology (gematria)
def name_to_numerology(name):
    numbers = [(ord(letter.upper()) - 64) % 9 + 1 for letter in name if letter.isalpha()]
    total = sum(numbers) % 9 + 1
    return total, DATA["numerology"].get(str(total), "No Data")

# Convert name to astrology code
def name_to_astrology(name):
    planets = [DATA["planets"].get(letter.upper(), "Unknown") for letter in name if letter.upper() in DATA["planets"]]
    most_common_planet = Counter(planets).most_common(1)
    dominant_planet = most_common_planet[0][0] if most_common_planet else "Unknown"
    return dominant_planet, DATA["astrology"].get(dominant_planet, "No Data")

# Generate psychological profile
def generate_psychology_analysis(name):
    name_hash = sum(ord(c) for c in name) % len(DATA["psychology"])
    return DATA["psychology"][name_hash]
