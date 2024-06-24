import cv2
import numpy as np
from tqdm import tqdm

def crop_and_rotate_video(video_path, angle, x1, y1, x2, y2, output_name=None):
    """
    Crops and rotates a video.

    Parameters:
    video_path (str): Path to the input video file.
    angle (float): Rotation angle in degrees.
    x1 (int): X-coordinate of the top-left corner of the crop box.
    y1 (int): Y-coordinate of the top-left corner of the crop box.
    x2 (int): X-coordinate of the bottom-right corner of the crop box.
    y2 (int): Y-coordinate of the bottom-right corner of the crop box.
    output_name (str, optional): Name of the output video file. If None, appends '_rotcrop' to the original name.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_width = x2 - x1
    output_height = y2 -y1 

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if output_name is None:
        output_name = video_path.split('.')[0] + '_rotcrop.mp4'
        
    out = cv2.VideoWriter(output_name, fourcc, 20.0, (output_width, output_height))

    for _ in tqdm(range(total_frames), desc="Rotating and cropping video"):
        ret, frame = cap.read()
        if not ret:
            break
        
        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv2.INTER_LINEAR)
        result = result[y1:y2, x1:x2]
        out.write(result)
  
    cap.release()
    out.release()
    cv2.destroyAllWindows()