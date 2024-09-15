import streamlit as st
import yt_dlp
import os

import download_video



title = st.title("The video downloader created with YouTube DL")
divider_1 = st.divider()

display_1 = False
url = st.text_input("Enter the url of the video", disabled=display_1)
download_button = st.button("Download", type="primary", disabled=display_1)



if download_button:
    location = download_video.download_video(url)
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