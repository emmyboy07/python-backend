from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load movie links from file
def load_movie_links():
    movies = {}
    file_path = "cleaned_links.txt"  # Ensure this file exists in the same directory as main.py

    # Check if the file exists
    if not os.path.exists(file_path):
        print("❌ ERROR: cleaned_links.txt NOT FOUND!")
        return {}

    print("📂 File exists. Reading file now...")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(.+?)\((\d{4})\) - (http.+)", line)
            if match:
                title, year, url = match.groups()
                movies[(title.lower().strip(), year.strip())] = url

    print(f"✅ Loaded {len(movies)} movies!")  # Debugging info

    if len(movies) > 0:
        first_movie = list(movies.keys())[0]
        print(f"🎬 First Movie: {first_movie} → {movies[first_movie]}")

    return movies

movies_db = load_movie_links()

@app.get("/get_movie_link")
async def get_movie_link(name: str, year: str):
    key = (name.lower().strip(), year.strip())
    print(f"🔍 Searching for: {key}")  # Debugging info

    if key in movies_db:
        return {"title": name, "year": year, "link": movies_db[key]}

    return {"error": "Movie not found"}
