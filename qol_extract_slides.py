# Detects unique slides from a presentation video and saves them as a PDF
import cv2
import os

# --- CONFIG ---
video_path = "your_video.mp4"       # path to your video file
output_pdf = "slides_output.pdf"     # name of the output PDF
temp_folder = "temp_slides"          # temp folder to hold slide images
sample_interval = 1                  # check every N seconds (1 = checks every second)
threshold = 0.95                     # similarity threshold, higher = more sensitive

# create temp folder for the individual slide images
os.makedirs(temp_folder, exist_ok=True)

# open video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_interval = int(fps * sample_interval)

print(f"Video FPS: {fps}")
print(f"Total frames: {total_frames}")
print(f"Checking every {sample_interval}s ({frame_interval} frames)")

cap.release()