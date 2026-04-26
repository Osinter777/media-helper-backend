from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, RedirectResponse
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "UMD Lite API backend работает"}

@app.get("/download")
def download(url: str = Query(...), media_type: str = Query("video")):
    try:
        api_url = "https://www.tikwm.com/api/"
        r = requests.get(api_url, params={"url": url})
        data = r.json()

        if data.get("code") != 0:
            return JSONResponse({"error": "TikTok API error"}, status_code=500)

        item = data.get("data", {})

        if media_type == "audio":
            file_url = item.get("music")
        else:
            file_url = item.get("play")

        if not file_url:
            return JSONResponse({"error": "No video found"}, status_code=500)

        return RedirectResponse(file_url)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)        try:
            r = requests.get(TIKWM_API, params={"url": url}, timeout=20)
            data = r.json()

            if data.get("code") != 0:
                return JSONResponse({"error": data.get("msg", "TikTok API error")}, status_code=500)

            item = data.get("data", {})

            return {
                "status": "ok",
                "source": "tikwm",
                "title": item.get("title"),
                "thumbnail": item.get("cover"),
                "duration": item.get("duration"),
                "webpage_url": url
            }

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    try:
        with yt_dlp.YoutubeDL({
            "quiet": True,
            "skip_download": True,
            "noplaylist": True
        }) as ydl:
            data = ydl.extract_info(url, download=False)

        return {
            "status": "ok",
            "source": "yt-dlp",
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

    if is_tiktok(url):
        try:
            r = requests.get(TIKWM_API, params={"url": url}, timeout=20)
            data = r.json()

            if data.get("code") != 0:
                return JSONResponse({"error": data.get("msg", "TikTok API error")}, status_code=500)

            item = data.get("data", {})

            if media_type == "audio":
                file_url = item.get("music")
            else:
                file_url = item.get("play") or item.get("wmplay")

            if not file_url:
                return JSONResponse({"error": "API не вернул файл"}, status_code=500)

            if file_url.startswith("/"):
                file_url = "https://www.tikwm.com" + file_url

            return RedirectResponse(file_url)

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

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
        return JSONResponse({"error": str(e)}, status_code=500)            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
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
