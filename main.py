from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Enable CORS for all origins (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and clean movie links
def load_movie_links():
    movies = {}
    with open("cleaned_links.txt", "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(.+?) \((\d{4})\) - (http.+)", line)
            if match:
                title, year, url = match.groups()
                movies[(title.lower().strip(), year.strip())] = url
    print(f"Loaded {len(movies)} movies!")  # Debugging info
    return movies

movies_db = load_movie_links()

@app.get("/get_movie_link")
async def get_movie_link(name: str, year: str):
    key = (name.lower().strip(), year.strip())

    if key in movies_db:
        return {"title": name, "year": year, "link": movies_db[key]}

    return {"error": "Movie not found"}
