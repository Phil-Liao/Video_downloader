import yt_dlp as _youtube_dl
import youtube_dl
def download_video(url):
  ydl_opts = {'outtmpl': 'video_files/%(title)s.%(ext)s',
              'cookiefile': 'cookies.firefox-private.txt',
              'http_headers': {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                },
              }
  with _youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
      result = ydl.extract_info("{}".format(url))
      title = result.get("title", None)
      return title

