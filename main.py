import yt_dlp
from fastapi import FastAPI

app = FastAPI()

@app.get("/download")
def get_video_info(url: str):
    # এখানে 'cookiefile' যোগ করতে হবে যাতে ইউটিউব ব্লক না করে
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt', 
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title', 'Unknown Title'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": info.get('url', '')
            }
    except Exception as e:
        return {"error": str(e)}
