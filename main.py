import re
import json
import random
import pandas as pd
from collections import Counter
from fastapi import FastAPI, HTTPException
import uvicorn
import supabase
import logging
from cachetools import TTLCache
from config import SUPABASE_URL, SUPABASE_KEY
from utils import name_to_runes, name_to_tarot, name_to_numerology, name_to_astrology, generate_psychology_analysis

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Supabase database connection
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Cache for optimizing repeated queries
cache = TTLCache(maxsize=1000, ttl=3600)  # Cache results for 1 hour

# Initialize FastAPI
app = FastAPI()

# Main function to analyze name
def analyze_name(name):
    name = re.sub(r'[^a-zA-Z]', '', name).strip()  # Remove non-alphabetic characters
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Check cache first
    if name in cache:
        logging.info(f"Cache hit for {name}")
        return cache[name]
    
    # Check Supabase database
    existing_entry = supabase_client.table("users_analysis").select("*").eq("name", name).execute()
    if existing_entry.data:
        result = json.loads(existing_entry.data[0]["result"])
        cache[name] = result  # Store in cache
        return result
    
    # Generate new analysis
    runes = name_to_runes(name)
    tarot = name_to_tarot(name)
    numerology, numerology_meaning = name_to_numerology(name)
    astrology, astrology_description = name_to_astrology(name)
    psychology = generate_psychology_analysis(name)

    result = {
        "Name": name,
        "Runic Analysis": runes,
        "Tarot Archetypes": tarot,
        "Numerology": {"Number": numerology, "Meaning": numerology_meaning},
        "Astrology": {"Planet": astrology, "Description": astrology_description},
        "Psychological Profile": psychology
    }
    
    # Store in database and cache
    supabase_client.table("users_analysis").insert({"name": name, "result": json.dumps(result)}).execute()
    cache[name] = result
    
    return result

@app.get("/analyze/{name}")
def analyze_name_api(name: str):
    return analyze_name(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
