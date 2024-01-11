import pytube
import os
import pandas as pd
from tqdm import tqdm

OUTPUT_DIR = "audio"
CSV_PATH = "annotations/eval_segments.csv"

def download_audio(video_id: str) -> None:
    youtube_url: str = f"https://www.youtube.com/watch?v={video_id}"
    video: pytube.YouTube = pytube.YouTube(youtube_url, use_oauth=True, allow_oauth_cache=True)
    audio_stream: pytube.Stream = video.streams.filter(only_audio=True).first()
    # print(type(audio_stream), audio_stream)
    audio_stream.download(output_path=OUTPUT_DIR)

def test_func() -> None:
    video_id: str = "jsnwmdhz9xI"
    download_audio(video_id)

def process_csv(csv_path: str = CSV_PATH) -> None:
    with open(csv_path, "r") as f:
        lines = f.readlines()
        lines = lines[3:] # exclude header
        
    for line in tqdm(lines, desc=f"Downloading audio in {csv_path}"):
        line = line.strip()
        line = line.split(",")
        video_id = line[0]
        try:
            download_audio(video_id)
        # except (KeyError, pytube.exceptions.VideoUnavailable) as e:
        except:
            print(f"Video {video_id} is unavailable...")
        

if __name__ == "__main__":
    process_csv()