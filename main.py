import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# সব ডোমেইন থেকে রিকোয়েস্ট অ্যালাউ করার জন্য CORS মিডলওয়্যার
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
def get_video_info(url: str):
    ydl_opts = {
        'format': 'best',
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
                    if f.get('url') and f.get('ext') == 'mp4':
                        download_url = f.get('url')
                        break
            
            return {
                "title": info.get('title', 'Unknown Title'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": download_url or info.get('url', '')
            }
    except Exception as e:
        return {"error": str(e)}
