from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, RedirectResponse
import yt_dlp

app = FastAPI()

SUPPORTED = [
    "youtube.com", "youtu.be",
    "tiktok.com",
    "instagram.com",
    "pinterest.",
    "likee.",
    "snapchat.com"
]

def check_url(url: str):
    return any(site in url.lower() for site in SUPPORTED)


@app.get("/")
def home():
    return {"status": "UMD Lite backend работает"}


@app.get("/info")
def info(url: str = Query(...)):
    if not check_url(url):
        return JSONResponse({"error": "Сайт не поддерживается"}, status_code=400)

    opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)

        return {
            "status": "ok",
            "title": data.get("title"),
            "thumbnail": data.get("thumbnail"),
            "duration": data.get("duration"),
            "webpage_url": data.get("webpage_url")
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/download")
def download(
    url: str = Query(...),
    media_type: str = Query("video")
):
    if not check_url(url):
        return JSONResponse({"error": "Сайт не поддерживается"}, status_code=400)

    if media_type == "audio":
        fmt = "bestaudio/best"
    else:
        fmt = "best"

    opts = {
        "quiet": True,
        "format": fmt,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)

        direct_url = data.get("url")

        if not direct_url:
            return JSONResponse({"error": "Не удалось получить ссылку"}, status_code=500)

        return RedirectResponse(direct_url)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
