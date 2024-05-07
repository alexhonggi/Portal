import cv2
import os
import time
import threading
import imageio

# Parameters
CHUNK_DURATION = 20  # Duration of each video chunk in seconds
PLAYBACK_DELAY = 60  # Increased delay before starting playback in seconds
FPS = 20  # Frames per second

def resize_frame(frame):
    """Resize frame to be divisible by 16 for codec compatibility."""
    height, width, _ = frame.shape
    adjusted_height = (height // 16) * 16
    adjusted_width = (width // 16) * 16
    return cv2.resize(frame, (adjusted_width, adjusted_height))

def capture_and_save():
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
        video_index += 1
        start_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def playback():
    time.sleep(PLAYBACK_DELAY)
    video_index = 0

    while True:
        video_file = f'output_{video_index}.mp4'
        if os.path.exists(video_file) and os.stat(video_file).st_size > 100:  # Check if file seems complete
            try:
                reader = imageio.get_reader(video_file)
                for frame in reader:
                    cv2.imshow('Playback', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                reader.close()
            except Exception as e:
                print(f"Error reading video file {video_file}: {e}")
            video_index += 1
        else:
            print(f"Waiting for video file {video_file} to be ready...")
            time.sleep(5)  # Wait before trying to read the file again

    cv2.destroyAllWindows()

thread = threading.Thread(target=capture_and_save)
thread.start()
playback()
thread.join()
