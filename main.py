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
    # কোনো নির্দিষ্ট ফরম্যাট বা এক্সটেনশন ফিল্টার ছাড়াই সবচেয়ে সেফ অপশন
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিংক বের করার উন্নত লজিক
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
