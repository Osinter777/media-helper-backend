from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
import yt_dlp
import tempfile
import os
import uuid

app = FastAPI()

SUPPORTED = [
    "tiktok.com",
    "instagram.com",
    "pinterest.",
    "likee.",
    "snapchat.com",
    "youtube.com",
    "youtu.be"
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
        "noplaylist": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.tiktok.com/"
        }
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
def download(url: str = Query(...), media_type: str = Query("video")):
    if not check_url(url):
        return JSONResponse({"error": "Сайт не поддерживается"}, status_code=400)

    temp_dir = tempfile.gettempdir()
    file_id = str(uuid.uuid4())

    if media_type == "audio":
        fmt = "bestaudio/best"
        ext = "mp3"
    else:
        fmt = "best[ext=mp4]/best"
        ext = "mp4"

    output_template = os.path.join(temp_dir, f"{file_id}.%(ext)s")

    opts = {
        "quiet": True,
        "format": fmt,
        "noplaylist": True,
        "outtmpl": output_template,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.tiktok.com/"
        }
    }

    if media_type == "audio":
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(data)

        if media_type == "audio":
            filename = os.path.splitext(filename)[0] + ".mp3"

        if not os.path.exists(filename):
            return JSONResponse({"error": "Файл не найден после загрузки"}, status_code=500)

        return FileResponse(
            filename,
            media_type="application/octet-stream",
            filename=os.path.basename(filename)
        )

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)            data = ydl.extract_info(url, download=False)

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
def download(url: str = Query(...), media_type: str = Query("video")):
    if not check_url(url):
        return JSONResponse({"error": "Сайт не поддерживается"}, status_code=400)

    temp_dir = tempfile.gettempdir()
    file_id = str(uuid.uuid4())

    if media_type == "audio":
        fmt = "bestaudio/best"
        ext = "mp3"
    else:
        fmt = "best[ext=mp4]/best"
        ext = "mp4"

    output_template = os.path.join(temp_dir, f"{file_id}.%(ext)s")

    opts = {
        "quiet": True,
        "format": fmt,
        "noplaylist": True,
        "outtmpl": output_template,
    }

    if media_type == "audio":
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(data)

        if media_type == "audio":
            filename = os.path.splitext(filename)[0] + ".mp3"

        if not os.path.exists(filename):
            return JSONResponse({"error": "Файл не найден после загрузки"}, status_code=500)

        return FileResponse(
            filename,
            media_type="application/octet-stream",
            filename=os.path.basename(filename)
        )

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)        with yt_dlp.YoutubeDL(opts) as ydl:
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
