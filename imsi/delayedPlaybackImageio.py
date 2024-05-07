import cv2
import os
import time
import threading
import imageio

# Parameters
CHUNK_DURATION = 60  # Duration of each video chunk in seconds
PLAYBACK_DELAY = 60  # Delay before starting playback in seconds
FPS = 20  # Frames per second

def capture_and_save():
    cap = cv2.VideoCapture(0)  # Start video capture
    video_index = 0
    start_time = time.time()

    while True:
        # Create a new video file at each chunk duration
        video_file = f'output_{video_index}.mp4'
        writer = imageio.get_writer(video_file, fps=FPS, codec='libx264', quality=8)

        print(f"Recording {video_file}")
        while time.time() - start_time < CHUNK_DURATION:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            writer.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert frame to RGB

        writer.close()
        video_index += 1
        start_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def playback():
    time.sleep(PLAYBACK_DELAY)  # Delay playback for specified seconds
    video_index = 0

    while True:
        video_file = f'output_{video_index}.mp4'
        if os.path.exists(video_file):
            reader = imageio.get_reader(video_file)
            for frame in reader:
                cv2.imshow('Playback', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Convert frame to BGR
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            reader.close()
            video_index += 1
        else:
            break

    cv2.destroyAllWindows()

# Start the capture/save thread
thread = threading.Thread(target=capture_and_save)
thread.start()

# Handle playback in the main thread
playback()

# Wait for the capture thread to finish
thread.join()
