import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math

def calculate_average_pixel_change(frame1, frame2):
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)
    
    # Calculate the average change per pixel
    avg_change = np.mean(diff)
    
    return avg_change

def process_video(video_path,
                  sample_rate=10,
                  end_time = None,
                  dir='plots',
                  prefix='YH'
                  filename='avg_pixel_change_plot.png',
                  clip_dir='clips'):
    os.makedirs(dir, exist_ok=True)
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if end_time is None:
        end_time = total_frames/fps
    
    # Read the first frame
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read first frame.")
        return
    
    # Initialize lists to store average pixel changes and corresponding times
    pixel_changes = []
    times = []
    
    frame_count = 0
    while True:
        # Calculate the time for the current frame
        time = frame_count / fps
        # Read the current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, current_frame = cap.read()
        if not ret or time > end_time:
            break
        
        # Calculate the average pixel change between the current frame and the previous frame
        avg_change = calculate_average_pixel_change(prev_frame, current_frame)
        pixel_changes.append(avg_change)
        
        # Calculate the time for the current frame
        time = frame_count / fps
        times.append(time)
    
        # Update the previous frame
        prev_frame = current_frame
        
        frame_count += sample_rate
        if frame_count % (sample_rate * 100) == 0:
            print(f"Processed {frame_count} frames")
    
    # Release the video capture object
    cap.release()
    # Plot the distribution of average pixel changes
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(pixel_changes, bins=50, color='blue', alpha=0.7)
    plt.xlabel('Average Pixel Change')
    plt.ylabel('Frequency')
    plt.title('Distribution of Average Pixel Change Between Consecutive Frames')
    
    plt.subplot(1, 2, 2)
    plt.plot([x/60 for x in times], pixel_changes, color='red')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Average Pixel Change')
    plt.title('Average Pixel Change vs. Time')
    
    output_plot = dir + '/' + filename
    plt.tight_layout()
    plt.savefig(output_plot)
    
    ############################################################################
    ## THIS SECTION OF CODE CLIPS ALL SECTIONS THAT EXCEED THE MEAN + STD DEV ##
    ## OF THE AVERAGE PIXEL CHANGE BETWEEN SECONDS OF VIDEO IN ORDER TO GET   ##
    ## CLIPS THAT INCLUDE A FISH                                              ##
    ############################################################################
    os.makedirs(clip_dir, exist_ok=True)
    
    # Convert time to frame number
    def time_to_frame(time):
        return int(time * fps)
    
    # Identify continuous peak locations
    continuous_segments = []
    start_idx = None
    threshold = np.mean(pixel_changes) + np.std(pixel_changes)
    
    for i, change in enumerate(pixel_changes):
        if change > threshold:
            if start_idx is None:
                start_idx = i
        else:
            if start_idx is not None:
                end_idx = i - 1
                if end_idx > start_idx + 4:
                    continuous_segments.append((start_idx, end_idx))
                start_idx = None
    
    # If the last segment goes to the end of the list
    if start_idx is not None:
        continuous_segments.append((start_idx, len(pixel_changes) - 1))
    
    # Clip the video around each continuous segment
    cap = cv2.VideoCapture(video_path)
    for segment in continuous_segments:
        start_time = times[segment[0]]
        end_time = times[segment[1]]
        
        start_frame = time_to_frame(start_time)
        end_frame = time_to_frame(end_time)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'{clip_dir}/{prefix}_clip_{math.floor(start_time)}_{math.floor(end_time)}.mp4', fourcc, fps, 
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        
        for frame_idx in range(start_frame, end_frame + 1):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        out.release()
    
    cap.release()

# Example usage
video_path = '/mnt/c/Users/attho/Downloads/0015_vid.mp4'
start = time.time()
process_video(video_path, sample_rate=150, end_time=None, dir='plots/', prefix='YH_s2_tr1', filename='avg_pix_YH_s2_tr1_bower.png', clip_dir='clips/YH_s2_tr1_bower_clips')
print(time.time() - start)