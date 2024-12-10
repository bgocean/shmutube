
import yt_dlp

def download_video(url, save_path="."):
    ydl_opts = {
        "outtmpl": f"{save_path}/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Пример использования
video_url = "https://www.youtube.com/shorts/FMjCIiL4ELI"
download_video(video_url)
