# Idea
# The concept is to create a buffer system that reads live video from a webcam, 
# saves it in one-minute chunks, and then plays back these chunks with a one-minute delay. 
# This kind of setup could be used for a variety of applications, 
# such as delayed video monitoring, performance analysis, or even for artistic installations 
# where live actions are replayed with a time shift.

# Implementation Steps
# Video Capture: Use OpenCV to capture video from the webcam.
# Chunk Saving: Save the video frames into files, each containing one minute of video. 
# This can be managed by tracking the time since the last save and starting a new file once one minute has elapsed.
# Playback with Delay: Start playing back the saved video files after a one-minute delay. 
# This means that for the first minute, the system will only capture and save data, not display it. 
# After the first minute, while continuing to capture and save new data, 
# the system will simultaneously start playing the first saved chunk.

# Instructions to Run the Code
# Installation: Ensure you have the opencv-python package installed (pip install opencv-python).
# Environment: This script assumes you have a webcam connected and accessible. 
# It also assumes your system supports the XVID codec for saving the video files.
# Operation: Run the script. It will start capturing video immediately and begin playback after a one-minute delay.

import cv2
import os
import time
import threading

# Parameters
CHUNK_DURATION = 60  # Duration of each video chunk in seconds
PLAYBACK_DELAY = 60  # Delay before starting playback in seconds
FPS = 20  # Frames per second

# Global queue to hold video filenames for playback
video_queue = []

def capture_and_save():
    cap = cv2.VideoCapture(0)  # Start video capture
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec definition
    frame_count = 0
    start_time = time.time()
    video_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count == 0:
            video_file = f'output_{video_index}.avi'
            out = cv2.VideoWriter(video_file, fourcc, FPS, (640, 480))
            video_index += 1
            video_queue.append(video_file)  # Add video for playback
            print(f"Recording {video_file}")

        out.write(frame)
        frame_count += 1

        if time.time() - start_time >= CHUNK_DURATION:
            out.release()
            frame_count = 0
            start_time = time.time()

    cap.release()
    out.release()

def playback():
    while True:
        if video_queue:
            video_file = video_queue.pop(0)
            cap = cv2.VideoCapture(video_file)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Playback', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()

# Start the capture/save thread
thread = threading.Thread(target=capture_and_save)
thread.start()

# Handle playback in the main thread
time.sleep(PLAYBACK_DELAY)
playback()

# Wait for the capture thread to finish
thread.join()
cv2.destroyAllWindows()
