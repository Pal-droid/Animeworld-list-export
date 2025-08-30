from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="AnimeWorld Watchlist Scraper")

class AnimeItem(BaseModel):
    title: str
    jtitle: str
    score: int
    episodes: int
    max_episodes: int
    status: str
    year: int
    genres: list[str]
    mal_link: str | None = None
    anilist_link: str | None = None
    mangaworld_link: str | None = None
    image: str | None = None
    notes: str | None = None

class UserResult(BaseModel):
    id: int
    username: str
    pfp: str

@app.get("/scrape/{user_id}")
def scrape_watchlist(user_id: int):
    url = f"https://www.animeworld.ac/watchlist/{user_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="User not found or private watchlist")

    soup = BeautifulSoup(resp.text, "html.parser")
    folders = soup.select(".watchlist-folder")

    result = {}

    for folder in folders:
        folder_name = folder.select_one("h4").text.split("(")[0].strip()
        folder_anime = []

        for item in folder.select(".watchlist-list-row.item"):
            title_tag = item.select_one(".title a")
            hidden_data = item.select_one(".hidden-data")
            hyperlinks = hidden_data.select_one(".hyperlinks") if hidden_data else None
            genres = [g.text for g in hidden_data.select(".categories a")] if hidden_data else []

            anime = AnimeItem(
                title=title_tag.text.strip() if title_tag else "",
                jtitle=title_tag['data-jtitle'] if title_tag else "",
                score=int(item['data-score']),
                episodes=int(item['data-episodes']),
                max_episodes=int(item['data-max-episodes']),
                status=item['data-state'],
                year=int(item['data-year']),
                genres=genres,
                mal_link=hyperlinks.select_one(".mal").text if hyperlinks and hyperlinks.select_one(".mal") else None,
                anilist_link=hyperlinks.select_one(".anilist").text if hyperlinks and hyperlinks.select_one(".anilist") else None,
                mangaworld_link=hyperlinks.select_one(".mangaworld").text if hyperlinks and hyperlinks.select_one(".mangaworld") else None,
                image=item.select_one(".thumb img")['src'] if item.select_one(".thumb img") else None,
                notes=hidden_data.select_one(".notes").text if hidden_data and hidden_data.select_one(".notes") else None
            )
            folder_anime.append(anime.dict())

        result[folder_name] = folder_anime

    return result

@app.get("/search/{username}")
def search_users(username: str):
    url = f"https://www.animeworld.ac/users?keyword={username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch search results")

    soup = BeautifulSoup(resp.text, "html.parser")
    users = []

    for item in soup.select(".film-list .item"):
        link = item.select_one("a.user-image")
        name_tag = item.select_one("a.name")
        img_tag = item.select_one("a.user-image img")

        if not link or not name_tag or not img_tag:
            continue

        # Extract user ID from the profile URL (e.g., /profile/184425)
        href = link.get("href", "")
        user_id = int(href.split("/")[-1]) if href.startswith("/profile/") else None

        user = UserResult(
            id=user_id,
            username=name_tag.text.strip(),
            pfp=img_tag.get("src", "")
        )
        users.append(user.dict())

    return {"results": users}
