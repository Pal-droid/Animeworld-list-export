# Animeworld list export
Animeworld list export is a FastAPI powered API that returns json metadata of a selected user's watch list on Animeworld.

---

## ✨ Features

- 🔎 **Search users** on AnimeWorld by username.  
- 📂 **Scrape user watchlists** including all folders:
  - In corso
  - Completati
  - In pausa
  - Droppati
  - Da guardare
- 📝 Extracts detailed anime information:
  - Titles (Italian & Japanese)
  - Score
  - Episodes watched / total episodes
  - Status (watching, completed, etc.)
  - Release year
  - Genres
  - External links (MAL, Anilist, MangaWorld)
  - Thumbnail image
  - User notes

---

## ⚡ Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/Pal-droid/Animeworld-list-export
cd Animeworld-list-export

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install fastapi uvicorn requests beautifulsoup4
```

---

▶️ Running the API

Start the server with:

```
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

📚 API Endpoints

🔍 Search Users

```http
GET /search/{username}
```

Example:

```http
GET /search/Palidk
```

Response:

```json
{
  "results": [
    {
      "id": 184425,
      "username": "Palidk",
      "pfp": "https://cdn.animeworld.ac/user/avatars/xyz.jpg"
    }
  ]
}
```

---

📂 Scrape Watchlist

```http
GET /scrape/{user_id}
```

Example:

```http
GET /scrape/184425
```

Response:

```json
{
  "In corso": [
    {
      "title": "Naruto Shippuden",
      "jtitle": "ナルト- 疾風伝",
      "score": 8,
      "episodes": 123,
      "max_episodes": 500,
      "status": "watching",
      "year": 2007,
      "genres": ["Azione", "Avventura", "Shounen"],
      "mal_link": "https://myanimelist.net/anime/1735/Naruto__Shippuuden",
      "anilist_link": "https://anilist.co/anime/1735",
      "mangaworld_link": null,
      "image": "https://cdn.animeworld.ac/thumbnails/naruto.jpg",
      "notes": "Rewatch in corso"
    }
  ],
  "Completati": [...],
  "Da guardare": [...]
}
```

---

⚠️ Disclaimer

This project is intended for educational and personal use only.
Scraping content from third-party websites may violate their Terms of Service. Use responsibly.


---

🛠 Tech Stack

FastAPI — API framework

Requests — HTTP client

BeautifulSoup4 — HTML parsing
