import os
import time
import json
from calc_avg_pixel_change import process_video  # Import the processing function
import subprocess

""" 
The script automates the processing of long-duration videos stored in a Dropbox directory
using rclone for file management. It lists the video files in each subdirectory, downloads
those exceeding a specified duration (10 hours), processes them to extract shorter clips,
and then deletes the local copies. Files listed in SKIP_FOLDERS are not downloaded.
"""

# Configuration
DROPBOX_REMOTE = 'CichlidPiData'  # Name of the rclone remote
# Path to your YH_Build directory in Dropbox
ROOT_DIRECTORY = '/BioSci-McGrath/Apps/CichlidPiData/__ProjectData/YH_Build'
DOWNLOAD_FOLDER = '/mnt/c/Users/attho/Downloads/'
VIDEO_THRESHOLD_SIZE = 10 * 60 * 60 * 1000  # 10 hours in milliseconds
SKIP_FOLDERS = ['YH_s1_tr1_BowerBuilding', 'YH_s1_tr2_BowerBuilding',
                'YH_s2_tr1_BowerBuilding', 'YH_s2_tr2_BowerBuilding']  # List of folders to skip


def list_files(remote_path):
    """List files in a remote directory using rclone."""
    try:
        result = subprocess.run(
            ['rclone', 'lsjson', f'{DROPBOX_REMOTE}:{remote_path}'], capture_output=True, text=True)
        result.check_returncode()
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as err:
        print(f"Error listing files in {remote_path}: {err}")
        print(f"rclone stderr: {result.stderr}")
        return []
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON for {remote_path}: {err}")
        print(f"rclone output: {result.stdout}")
        return []


def download_file(remote_path, local_path):
    """Download a file from the remote using rclone."""
    result = subprocess.run(
        ['rclone', 'copy', f'{DROPBOX_REMOTE}:{remote_path}', local_path])
    return result.returncode == 0


def delete_file(local_path):
    """Delete a local file."""
    try:
        os.remove(local_path)
        print(f'Deleted file {local_path}')
    except OSError as err:
        print(f'Error deleting file {local_path}: {err}')


def process_directory(directory_path):
    """Process videos in the specified directory."""
    videos_path = os.path.join(ROOT_DIRECTORY, directory_path, 'Videos')
    files = list_files(videos_path)

    n_clips = 0
    for file_metadata in files:
        # 10+ hour video in milliseconds
        if file_metadata.get('Size', 0) > VIDEO_THRESHOLD_SIZE:
            file_path = os.path.join(videos_path, file_metadata['Path'])
            local_file_path = os.path.join(
                DOWNLOAD_FOLDER, os.path.basename(file_path))

            if download_file(file_path, DOWNLOAD_FOLDER):
                prefix = file_path
                n_clips += process_video(local_file_path,
                              sample_rate=150,
                              end_time=None,
                              dir='/home/athomas314/gatech/cs8903_research/plots/',
                              prefix=os.path.basename(directory_path)[:10])
                delete_file(local_file_path)
                if n_clips > 5:
                    break  # Process until you have five clips per directory


def main():
    # List all subdirectories in the root directory
    subdirectories = list_files(ROOT_DIRECTORY)

    for subdirectory in subdirectories:
        subdirectory_path = subdirectory['Path']
        folder_name = os.path.basename(subdirectory_path)

        if folder_name in SKIP_FOLDERS:
            print(f'Skipping folder: {subdirectory_path}')
            continue

        print(f'Processing subdirectory: {subdirectory_path}')
        process_directory(subdirectory_path)


if __name__ == "__main__":
    main()
