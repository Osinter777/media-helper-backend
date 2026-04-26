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
        return JSONResponse({"error": str(e)}, status_code=500)
