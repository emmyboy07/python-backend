from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import os
from difflib import get_close_matches

app = FastAPI()

# Enable CORS for frontend requests
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
    file_path = "cleaned_links.txt"  # Make sure this file is in the same directory

    if not os.path.exists(file_path):
        print("❌ ERROR: cleaned_links.txt NOT FOUND!")
        return {}

    print("📂 File exists. Reading file now...")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(.+?)\((\d{4})\) - (http.+)", line)
            if match:
                title, year, url = match.groups()
                title = title.lower().strip()
                movies[(title, year.strip())] = url

    print(f"✅ Loaded {len(movies)} movies!")  # Debugging info
    return movies

movies_db = load_movie_links()

def find_best_match(user_input, movie_list):
    """Finds the best matching movie title from the list."""
    matches = get_close_matches(user_input.lower(), [title for title, _ in movie_list], n=1, cutoff=0.5)
    return matches[0] if matches else None

@app.get("/get_movie_link")
async def get_movie_link(name: str = Query(...), year: str = Query(...)):
    name = name.lower().strip()
    year = year.strip()

    # Try exact match first
    if (name, year) in movies_db:
        return {"title": name, "year": year, "link": movies_db[(name, year)]}

    # Try fuzzy matching (find closest match)
    best_match = find_best_match(name, movies_db.keys())
    if best_match and (best_match, year) in movies_db:
        return {"title": best_match, "year": year, "link": movies_db[(best_match, year)]}

    return {"error": "Movie not found"}
