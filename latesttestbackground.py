import cv2
import numpy as np

# Load the background image
background_image = cv2.imread('C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\Uranus lol\\Uranus.jpg')

# Initialize video reader and writer
video = cv2.VideoCapture('C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\Uranus lol\\UranusOriginal.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Set output video dimensions to 9:16 ratio for YouTube Short
output_width = 474
output_height = int(output_width * (16 / 9))  # Calculate the height for a 9:16 aspect ratio
out = cv2.VideoWriter('C:\\Users\\eoint\\OneDrive\\Desktop\\Shortking retort\\Uranus lol\\output.mp4', fourcc, fps, (output_width, output_height))

# Add black borders to the background image to make it fit the portrait frame
top_border_height = (output_height - background_image.shape[0]) // 2
bottom_border_height = output_height - background_image.shape[0] - top_border_height
background_portrait = cv2.copyMakeBorder(background_image, top_border_height, bottom_border_height, 0, 0, cv2.BORDER_CONSTANT)

# Resize factor for the video - adjusted to fit the background image dimensions
resize_width = output_width // 2  # Half the width of the background
resize_height = background_image.shape[0]  # Full height of the background
darkness_tolerance = (30, 30, 30)  # Example tolerance values, this should be a tuple

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Resize video frame to fit the new dimensions
    frame_resized = cv2.resize(frame, (resize_width, resize_height))

    # Convert frame to grayscale and then to binary image using a threshold to create a mask
    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_frame, 1, 255, cv2.THRESH_BINARY)

    # Invert the mask to get the foreground
    mask_inv = cv2.bitwise_not(mask)

    # Isolate the foreground of the video frame from the background
    video_foreground = cv2.bitwise_and(frame_resized, frame_resized, mask=mask)
    
    # Isolate the background where the video will be placed
    roi_background = background_portrait[-resize_height:, :resize_width]
    background_without_video = cv2.bitwise_and(roi_background, roi_background, mask=mask_inv)
    
    # Add the video foreground on top of the background
    combined = cv2.add(background_without_video, video_foreground)
    background_portrait[-resize_height:, :resize_width] = combined
    
    # Write the frame
    out.write(background_portrait)

# Release everything
video.release()
out.release()
cv2.destroyAllWindows()