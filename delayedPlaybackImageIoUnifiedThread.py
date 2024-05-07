import cv2
import os
import time
import threading
import imageio

# Parameters
CHUNK_DURATION = 10  # Duration of each video chunk in seconds
PLAYBACK_DELAY = 30  # Delay before starting playback in seconds
FPS = 20  # Frames per second

def resize_frame(frame):
    """Resize frame to be divisible by 16 for codec compatibility."""
    height, width, _ = frame.shape
    adjusted_height = (height // 16) * 16
    adjusted_width = (width // 16) * 16
    return cv2.resize(frame, (adjusted_width, adjusted_height))

def capture_and_save(queue):
    cap = cv2.VideoCapture(0)  # Start video capture
    video_index = 0
    start_time = time.time()

    while True:
        video_file = f'output_{video_index}.mp4'
        writer = imageio.get_writer(video_file, fps=FPS, codec='libx264', quality=8)
        print(f"Recording {video_file}")
        
        while time.time() - start_time < CHUNK_DURATION:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            frame = resize_frame(frame)
            writer.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        writer.close()
        print(f"Finished recording {video_file}")
        queue.append(video_file)  # Append video file to the queue
        video_index += 1
        start_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def playback(queue):
    time.sleep(PLAYBACK_DELAY)
    while queue:
        video_file = queue.pop(0)
        try:
            reader = imageio.get_reader(video_file)
            for frame in reader:
                cv2.imshow('Playback', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            reader.close()
        except Exception as e:
            print(f"Error reading video file {video_file}: {e}")

    cv2.destroyAllWindows()

# Shared queue for videos
video_queue = []

# Start the capture/save thread
capture_thread = threading.Thread(target=capture_and_save, args=(video_queue,))
capture_thread.start()

# Handle playback in the main thread
playback(video_queue)

# Wait for the capture thread to finish
capture_thread.join()
