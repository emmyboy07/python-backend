from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import os

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load movie links
def load_movie_links():
    movies = {}
    file_path = "cleaned_links.txt"  # Ensure this file exists

    if not os.path.exists(file_path):
        print("❌ ERROR: cleaned_links.txt NOT FOUND!")
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(.+?) \((\d{4})\) - (http.+)", line)
            if match:
                title, year, url = match.groups()
                movies[(title.lower().strip(), year.strip())] = url

    print(f"✅ Loaded {len(movies)} movies!")  # Debugging info
    return movies

movies_db = load_movie_links()

@app.get("/get_movie_link")
async def get_movie_link(name: str = Query(...), year: str = Query(...)):
    key = (name.lower().strip(), year.strip())
    print(f"🔍 Searching for: {key}")  # Debugging info

    if key in movies_db:
        return {"title": name, "year": year, "link": movies_db[key]}

    return {"error": "Movie not found"}
