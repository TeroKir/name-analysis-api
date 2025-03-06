#!/bin/bash

# Deploy to Heroku or Render

# Step 1: Log in to Heroku (if using Heroku)
echo "Logging into Heroku..."
heroku login

# Step 2: Set up Heroku App
echo "Creating Heroku App..."
heroku create name-analysis-api

echo "Setting environment variables..."
heroku config:set SUPABASE_URL="your-supabase-url" SUPABASE_KEY="your-supabase-key"

# Step 3: Push code to Heroku
echo "Deploying to Heroku..."
git add .
git commit -m "Deploying API"
git push heroku main

# Step 4: Open the app
echo "Opening the deployed application..."
heroku open
