import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import argparse

def calculate_average_pixel_change(frame1, frame2):
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)
    
    # Calculate the average change per pixel
    avg_change = np.mean(diff)
    
    return avg_change

def process_video(video_path,
                  sample_rate=10,
                  end_time = None,
                  dir='plots/',
                  prefix='YH_',
                  filename='avg_pixel_change_plot.png',
                  clip_dir='clips/',
                  threshold_devs=1):
    start = time.time()
    os.makedirs(dir, exist_ok=True)
    # Open the video file
    video_name = video_path.split('/')[-1].split('.')[0]
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
        current_time = frame_count / fps
        # Read the current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, current_frame = cap.read()
        if not ret or current_time > end_time:
            break
        
        # Calculate the average pixel change between the current frame and the previous frame
        avg_change = calculate_average_pixel_change(prev_frame, current_frame)
        pixel_changes.append(avg_change)
        
        # Calculate the current_time for the current frame
        current_time = frame_count / fps
        times.append(current_time)
    
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
    
    output_plot = dir + prefix + filename
    plt.tight_layout()
    plt.savefig(output_plot)
    
    ############################################################################
    ## THIS SECTION OF CODE CLIPS ALL SECTIONS THAT EXCEED THE MEAN + STD DEV ##
    ## OF THE AVERAGE PIXEL CHANGE BETWEEN SECONDS OF VIDEO IN ORDER TO GET   ##
    ## CLIPS THAT INCLUDE A FISH                                              ##
    ############################################################################
    os.makedirs(clip_dir+prefix, exist_ok=True)
    
    # Convert current_time to frame number
    def current_time_to_frame(current_time):
        return int(current_time * fps)
    
    # Identify continuous peak locations
    continuous_segments = []
    start_idx = None
    threshold = np.mean(pixel_changes) + threshold_devs * np.std(pixel_changes)
    n_clips = 0
    total_extracted_time = 0
    for i, change in enumerate(pixel_changes):
        if change > threshold:
            if start_idx is None:
                start_idx = i
        else:
            if start_idx is not None:
                end_idx = i - 1
                if end_idx > start_idx + 4:
                    continuous_segments.append((start_idx, end_idx))
                    n_clips += 1
                    total_extracted_time += times[end_idx] - times[start_idx]
                start_idx = None
    
    # If the last segment goes to the end of the list
    if start_idx is not None:
        continuous_segments.append((start_idx, len(pixel_changes) - 1))
        total_extracted_time += times[len(pixel_changes) - 1] - times[start_idx]
    
    # Clip the video around each continuous segment
    cap = cv2.VideoCapture(video_path)
    for segment in continuous_segments:
        start_time = times[segment[0]]
        end_time = times[segment[1]]
        
        start_frame = current_time_to_frame(start_time)
        end_frame = current_time_to_frame(end_time)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'{clip_dir}{prefix}/{prefix}{video_name}_clip_{math.floor(start_time)}_{math.floor(end_time)}.mp4', fourcc, fps, 
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        
        for frame_idx in range(start_frame, end_frame + 1):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        out.release()
    
    cap.release()
    print(time.time() - start)
    print(f"Total extracted video time: {total_extracted_time / 60:.2f} minutes")
    return n_clips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video to calculate average pixel changes and extract clips with significant changes.")
    parser.add_argument("video_path", type=str, help="Path to the input video file ex. /mnt/c/Users/<username>/Downloads/<clip_name>.mp4")
    parser.add_argument("-s", "--sample_rate", type=int, default=150, help="Frame sampling rate (default: 150 (every 5 seconds @ 30fps))")
    parser.add_argument("-e","--end_time", type=float, default=None, help="End time in seconds (default: None - end of video)")
    parser.add_argument("-d","--dir", type=str, default="plots/", help="Directory to save plots (default: 'plots/')")
    parser.add_argument("-p","--prefix", type=str, default="YH_", help="Prefix for clip filenames (make sure to add trailing '_' for readability) (default: 'YH_', ex. 'YH_s1_tr1_')")
    parser.add_argument("-f","--filename", type=str, default="avg_pixel_change_plot.png", help="Filename for the plot (default: 'avg_pixel_change_plot.png')")
    parser.add_argument("-c","--clip_dir", type=str, default="clips/", help="Directory to save video clips (default: ''clips/')")
    parser.add_argument("-t","--threshold_devs", type=float, default=1, help="number of standard deviations above the mean to set the threshold (default = 1)")

    args = parser.parse_args()
    
    process_video(args.video_path, args.sample_rate, args.end_time, args.dir, args.prefix, args.filename, args.clip_dir, args.threshold_devs)