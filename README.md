# Name Analysis API

## Overview
This project is an API that analyzes a person's name using runes, tarot, numerology, astrology, and psychological profiling.

## Features
- **Runic Analysis**: Extracts meaning from the letters of a name based on ancient runes.
- **Tarot Archetypes**: Associates name patterns with major arcana archetypes.
- **Numerology**: Converts letters into numbers to determine personality traits.
- **Astrological Influence**: Maps name letters to planetary energies.
- **Psychological Profile**: Uses Jungian archetypes and the Big Five personality model.

## Technologies Used
- **Python 3.13**
- **FastAPI** (Backend API Framework)
- **Supabase** (Database)
- **Cachetools** (Caching)
- **Uvicorn** (ASGI Server)
- **Docker** (Containerization)
- **Heroku/Render** (Deployment)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/name-analysis.git
   cd name-analysis
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the application locally:**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Deployment
### **Using Docker:**
1. **Build the Docker image:**
   ```sh
   docker build -t name-analysis-api .
   ```
2. **Run the container:**
   ```sh
   docker run -p 8000:8000 name-analysis-api
   ```

### **Deploying to Heroku:**
1. **Login to Heroku CLI:**
   ```sh
   heroku login
   ```
2. **Create a new Heroku app:**
   ```sh
   heroku create name-analysis-api
   ```
3. **Push to Heroku:**
   ```sh
   git push heroku main
   ```

## API Endpoints
### **Analyze a Name**
**GET /analyze/{name}**
```json
{
  "Name": "Alex",
  "Runic Analysis": ["Ansuz", "Laguz", "Eiwaz"],
  "Tarot Archetypes": ["The Magician", "The High Priestess"],
  "Numerology": {"Number": 7, "Meaning": "Intellectual, introspective, spiritual"},
  "Astrology": {"Planet": "Mercury", "Description": "Communication, intelligence, adaptability"},
  "Psychological Profile": "Analytical thinker with deep introspection"
}
```

## License
This project is licensed under the MIT License.
