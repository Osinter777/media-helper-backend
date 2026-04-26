from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional
from urllib.parse import urlparse
from cachetools import TTLCache
import httpx

app = FastAPI()

cache = TTLCache(maxsize=1000, ttl=1800)

class MediaRequest(BaseModel):
    url: HttpUrl

class MediaResponse(BaseModel):
    ok: bool
    platform: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    media_type: Optional[str] = None
    direct_url: Optional[str] = None
    source_url: str
    error: Optional[str] = None

def detect_platform(url: str):
    host = urlparse(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "instagram.com" in host:
        return "instagram"
    if "tiktok.com" in host:
        return "tiktok"
    if "snapchat.com" in host:
        return "snapchat"
    if "likee" in host:
        return "likee"
    if "pinterest" in host:
        return "pinterest"
    return "unknown"

async def fetch_youtube(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"}
        )
    if r.status_code != 200:
        return MediaResponse(ok=False, platform="youtube", source_url=url, error="No data")

    data = r.json()
    return MediaResponse(
        ok=True,
        platform="youtube",
        title=data.get("title"),
        thumbnail=data.get("thumbnail_url"),
        media_type="video",
        source_url=url
    )

@app.post("/resolve", response_model=MediaResponse)
async def resolve(req: MediaRequest):
    url = str(req.url)

    if url in cache:
        return cache[url]

    platform = detect_platform(url)

    if platform == "youtube":
        result = await fetch_youtube(url)
    else:
        result = MediaResponse(
            ok=True,
            platform=platform,
            source_url=url,
            media_type="unknown"
        )

    cache[url] = result
    return result
