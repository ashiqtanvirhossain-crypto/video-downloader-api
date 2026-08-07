import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
def get_video_info(url: str):
    # ইউটিউবের ফরম্যাট এরর এড়াতে 'best' বা খালি রাখা সবচেয়ে নিরাপদ
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            download_url = info.get('url')
            if not download_url and 'formats' in info:
                for f in info['formats']:
                    if f.get('url'):
                        download_url = f.get('url')
                        break
            
            return {
                "title": info.get('title', 'Unknown Title'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": download_url or info.get('url', '')
            }
    except Exception as e:
        return {"error": str(e)}
