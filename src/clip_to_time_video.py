import cv2

def clip_to_time(video_path, start_time, end_time, output_path):
    """
    Clips a segment from a video file based on the specified start and end times and saves it to a new file.

    Parameters:
    video_path (str): The path to the input video file.
    start_time (float): The start time in seconds for the segment to clip.
    end_time (float): The end time in seconds for the segment to clip.
    output_path (str): The path to save the clipped video segment.

    Returns:
    str: The path to the saved clipped video file.

    Example usage:
    video_path = "/path/to/input/video.mp4"
    start_time = 1020  # in seconds
    end_time = 1080    # in seconds
    output_path = "/path/to/output/clipped_video.mp4"

    clip_to_time(video_path, start_time, end_time, output_path)
    """
    cap = cv2.VideoCapture(video_path) #(but really no cap tho)

    # Get the frames per second (fps) of the input video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Get width and height of video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec if necessary
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Set the starting frame of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    current_frame = start_frame
    while cap.isOpened() and current_frame <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Release everything if job is finished
    cap.release()
    out.release()
    return output_path