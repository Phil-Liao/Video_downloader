import yt_dlp as _youtube_dl
import youtube_dl
def download_video(url):
  ydl_opts = {'outtmpl': 'video_files/%(title)s.%(ext)s'}
  with _youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
      result = ydl.extract_info("{}".format(url))
      title = result.get("title", None)
      return title

