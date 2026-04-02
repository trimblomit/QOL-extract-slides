# Video Slides to PDF

This script detects unique slides from a slide-based presentation video 
and saves them into a single PDF.

It is useful when you have a lecture, webinar, meeting recording, or 
presentation video, but do not have the original slide deck or PDF copy.

---

## What it does

The script:

1. Opens a video file
2. Checks frames at a chosen time interval
3. Compares each checked frame to the last saved slide
4. Saves frames that look different enough to count as a new slide
5. Combines all detected slide images into one PDF
6. Deletes the temporary slide images after the PDF is created

---

## Requirements

Install these Python packages:

    pip install opencv-python Pillow