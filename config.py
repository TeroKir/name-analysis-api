import os

# Supabase Credentials (Replace with your actual credentials)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-key")

# API Settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True
