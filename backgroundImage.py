import cv2
import numpy as np

def select_background(frame_count, fps):
    time = frame_count / fps
    if time < 7:
        return 0
    elif 7 <= time < 20:
        return 1
    elif 20 <= time < 24:
        return 2
    elif 24 <= time < 28:
        return 3
    elif 28 <= time < 40:
        return 4
    elif 40 <= time < 45:
        return 5
    elif 45 <= time < 50:
        return 6
    elif 50 <= time < 55:
        return 7
    elif 55 <= time < 60:
        return 5  # background6 again as per your specification
    else:
        return 0  # Default to first image if time exceeds 60 seconds

# Load and resize background images
background_images = [cv2.imread(f'C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\background{i}.jpg') for i in range(1, 9)]
background_images = [cv2.resize(img, (360, 640)) for img in background_images]  # Resize all images to 360x640

# Initialize video reader and writer
video = cv2.VideoCapture('C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\your_video.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\output.mp4', fourcc, fps, (360, 640))

# Resize factor for the video (70% of original size)
resize_factor = 0.5
darkness_tolerance = np.array([30, 30, 30])  # Example tolerance values

# Process each frame
frame_count = 0
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Resize video frame
    frame_resized = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

    # Create a frame to hold the resized video in the bottom left corner of the background
    bottom_left_frame = np.zeros((640, 360, 3), dtype=np.uint8)

    # Calculate offsets for the bottom left corner
    x_offset = 0  # For bottom left corner, x_offset is 0
    y_offset = 640 - frame_resized.shape[0]  # For bottom left, y_offset is the height of the frame minus the height of the video

    # Position the resized video in the bottom left corner
    bottom_left_frame[y_offset:y_offset+frame_resized.shape[0], x_offset:x_offset+frame_resized.shape[1]] = frame_resized

    # Select the current background image based on frame_count
    current_background = background_images[select_background(frame_count, fps)]

    # Find pixels that are darker than the tolerance
    black_pixels = np.all(bottom_left_frame <= darkness_tolerance, axis=-1)

    # Replace black pixels with background
    bottom_left_frame[black_pixels] = current_background[black_pixels]
    
    # Write the frame
    out.write(bottom_left_frame)
    frame_count += 1

# Release everything
video.release()
out.release()
cv2.destroyAllWindows()


# 8 seconds to  20 seconds joe rogan
# charles the second 20 to 24
# charles the third 24 to 28
# farquad 28 to 42
# Prince 41 to 45 
# kevin hart 45 to 50 
# sith 50 to 55
# prince 55 to 60

