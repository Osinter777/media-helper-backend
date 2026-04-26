from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, RedirectResponse
import requests

app = FastAPI()

TIKWM_API = "https://www.tikwm.com/api/"

def is_tiktok(url: str):
    return "tiktok.com" in url.lower()

@app.get("/")
def home():
    return {
        "status": "UMD Lite работает",
        "support": "TikTok"
    }

@app.get("/download")
def download(url: str = Query(...), media_type: str = Query("video")):

    if not is_tiktok(url):
        return JSONResponse({
            "error": "Поддерживается только TikTok"
        }, status_code=400)

    try:
        r = requests.get(TIKWM_API, params={"url": url}, timeout=10)
        data = r.json()

        if data.get("code") != 0:
            return JSONResponse({
                "error": "TikTok API error",
                "response": data
            }, status_code=500)

        item = data.get("data", {})

        file_url = item.get("music") if media_type == "audio" else item.get("play")

        if not file_url:
            return JSONResponse({
                "error": "TikTok API не вернул файл",
                "response": data
            }, status_code=500)

        return RedirectResponse(file_url)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)            file_url = item.get("music") if media_type == "audio" else item.get("play")

            if not file_url:
                return JSONResponse({"error": "TikTok API не вернул файл", "response": data}, status_code=500)

            return RedirectResponse(file_url)

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    if is_youtube(url):
        if not YOUTUBE_API_URL or not YOUTUBE_API_KEY:
            return JSONResponse({
                "error": "YouTube API не настроен",
                "need": "Добавь YOUTUBE_API_URL и YOUTUBE_API_KEY в Render"
            }, status_code=500)

        try:
            headers = {
                "X-RapidAPI-Key": YOUTUBE_API_KEY,
                "X-RapidAPI-Host": "youtube-quick-video-downloader-free-api-download-all-video.p.rapidapi.com"
            }

            r = requests.get(
                YOUTUBE_API_URL,
                headers=headers,
                params={"url": url},
                timeout=30
            )

            data = r.json()

            file_url = (
                data.get("url")
                or data.get("link")
                or data.get("download")
                or data.get("download_url")
                or data.get("video")
                or data.get("data", {}).get("url")
                or data.get("data", {}).get("link")
                or data.get("data", {}).get("download_url")
            )

            if not file_url:
                return JSONResponse({
                    "error": "YouTube API не вернул ссылку",
                    "response": data
                }, status_code=500)

            return RedirectResponse(file_url)

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    return JSONResponse({
        "error": "Поддерживаются только TikTok и YouTube"
    }, status_code=400)
