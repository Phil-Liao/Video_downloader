import streamlit as st
import yt_dlp as youtube_dl
import os


def download_video(url):
  ydl_opts = {'outtmpl': 'video_files/the_video.%(ext)s',
              'cookiesfrombrowser': ('chrome',),
              'cookiefile': 'cookies.firefox-private.txt',
              'http_headers': {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                },
              }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
      result = ydl.extract_info("{}".format(url))
      title = result.get("title", None)
      return title

title = st.title("The video downloader created with YouTube DL")
divider_1 = st.divider()

display_1 = False
url = st.text_input("Enter the url of the video", disabled=display_1)
download_button = st.button("Download", type="primary", disabled=display_1)


if download_button:
    location = download_video(url)
    display_1 = True
    with open(f"video_files/{location}.mp4", "rb") as file:
        download_file = st.download_button(
            label="Download MP4",
            data=file,
            file_name=location,
            mime="video/mp4",
            type='primary'
        )
    os.remove(f"video_files/{location}.mp4") 