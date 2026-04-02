# Detects unique slides from a presentation video and saves them as a PDF
import cv2
import os
from PIL import Image

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

def compare_frames(frame_a, frame_b):
    """
    Compare two frames and return a similarity score between 0 and 1.
    Works by converting both to grayscale, resizing to a small standard size
    (so it's fast and ignores tiny pixel differences), then comparing
    using normalised correlation = basically how similar are the pixel patterns.
    1.0 = identical, 0.0 = completely different.
    """
    # convert to grayscale (colour doesn't matter for slide detection)
    gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
    # resize both to a small size so comparison is fast
    small_a = cv2.resize(gray_a, (320, 240))
    small_b = cv2.resize(gray_b, (320, 240))
    # gives a similarity score between the two images
    result = cv2.matchTemplate(small_a, small_b, cv2.TM_CCOEFF_NORMED)
    # result is a single value array
    similarity = result[0][0]
    return similarity

# --- Main loop ---
# list to store the file paths of each unique slide image
slide_paths = []
# this holds the last saved slide frame for comparing
previous_slide = None
slide_count = 0

for frame_number in range(0, total_frames, frame_interval):
    # jump to the frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        # if very first frame, always save it as slide 1
        if previous_slide is None:
            is_new_slide = True
        else:
            # compare current frame to the last saved slide
            similarity = compare_frames(frame, previous_slide)
            is_new_slide = similarity < threshold
        if is_new_slide:
            slide_count += 1
            filename = os.path.join(temp_folder, f"slide_{slide_count:03d}.png")
            cv2.imwrite(filename, frame)
            slide_paths.append(filename)
            previous_slide = frame
            # show progress
            timestamp = int(frame_number / fps)
            mins = timestamp // 60
            secs = timestamp % 60
            print(f"Slide {slide_count} detected at {mins:02d}m{secs:02d}s")

cap.release()

# --- Create PDF ---
if len(slide_paths) > 0:
    # open each slide image with pillow and convert to RGB (PDF needs RGB, not BGRA)
    images = [Image.open(path).convert("RGB") for path in slide_paths]
    # save first image as PDF, append rest as extra pages
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"\nComplete. {slide_count} slides saved to '{output_pdf}'")
else:
    print("\nNo slides detected. Check threshold.")