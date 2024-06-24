import cv2

def clip_to_time(video_path, start_time, end_time, output_path):
    #start time in seconds
    # end time in seconds
    cap = cv2.VideoCapture(video_path)

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

# # Example usage
# video_path = "/mnt/c/Users/attho/Downloads/MC_singlenuc23_1_Tk33_0212200003_vid_clip_36170_38240.mp4"
# start_time = 1020  # in seconds
# end_time = 1080    # in seconds
# output_path = '/mnt/c/Users/attho/Downloads/MC_singlenuc23_1_Tk33_0212200003_vid_debugging_clip.mp4'

# clip_to_time(video_path, start_time, end_time, output_path)
