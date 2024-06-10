## README - Deeplabcut setup for Cichlid Bower Repository

<!-- omit in toc -->
## Table of Contents
 - [Calculate Average Pixel Changes](#calculate-average-pixel-changes)
 - [Image Augmentation](#image-augmentation)
 - [Pull And Process](#pull-and-process)

 

### Calculate Average Pixel Changes
The goal of this script is to condense a 10 hour video into smaller clips that contain fish
in them. The script works by comparing the average change in pixel values between frames, 
and selecting and cropping out sections of video that have larger changes in pixel values. 
Anecdotablly, this works to roughly get a selection of clips that a fish is present in the 
frame. This can be used in conjunction with Deeplabcut to reduce the processing time needed 
to extract frames from images, or to simply as a preprocessing method to reduce the memory
footprint of the videos to prepare them for other processing methods. 

Make sure to provide a path to the script to process the video, and run 
`python calc_avg_pixel_change.py --help` in order to see the command line options.

### Image Augmentation
![Image augmentation](documentation/Image_aug_flowchart.png)
This script performs data augmentation on a dataset of images by applying random color transformations and 
optionally converting the images to grayscale. The purpose is to enhance the dataset for training neural networks, 
ensuring that the network does not rely on the color of the images to make predictions.

Usage:
    python image_augmentation.py input_folder output_folder --num_augmentations 5 --include_grayscale

Arguments:
* input_folder (str): Path to the input folder containing images.
* output_folder (str): Path to the output folder to save augmented images.
* --num_augmentations (int): Number of augmentations to perform per image (default is 5).
* --include_grayscale (flag): Include grayscale conversion of images if set.

Functions:
* parse_args(): Parses command-line arguments.
* random_color_augmentation(image): Applies random color transformations to an image.
* convert_to_grayscale(image): Converts an image to grayscale.
* augment_dataset(input_folder, output_folder, num_augmentations=5, include_grayscale=False): 
  * Augments the dataset with color transformations and optionally includes grayscale images.

### Google Colab Walkthrough
Once you have labelled your dataset and generated a training dataset following the DLC 
instructions you're ready to begin training models, you can do this locally if you have
a GPU, but if you do not a simple way to get access to a GPU is to use Google Colab. 
The steps below walk through how to train a DLC model on google colab.
 
1. Copy DLC project to google drive
2. Open google colab and mount your drive
	- ![mount drive](walkthrough_images/Mount_Drive.png)
3. Edit the project_path field in the config.yaml file to your new project location 
   in google drive
	- ex. /content/drive/My Drive/Research/<project_name>
4. edit the project path field in dlc-models/iteration-0/<project_name>/train/pose_cfg.yaml
	- you may also have to update the init_weights field depending on whether you are
	using the same version of python between your local setup that generated this file
	and google colab. I had to update it from python3.8 to python3.10
5. To run on a GPU, select the desired runtime in the top right corner of the colab notebook
	- ![select runtime](walkthrough_images/colab_runtime.png)
6. run the Google colab notebook 
7. Expect quite long runtimes (many hours)

### Setting up DLC on SRG Computer
1. get access by emailing support@cos.gatech.edu and state that you are working with the McGrath Lab and need to be added to the McGrath lab group.
2. once you get access you can ssh into the computer via your `<gt-username>@srg.biology.gatech.edu`
	- login with your gatech.edu password
3. once logged in execute the following commands to install miniconda 
	- NOTE: this can be skipped if your terminal looks like `(base) [<gt_username>@biocomputesrg]`, the `(base)` means that conda is already installed
	- `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
	- `bash Miniconda3-latest-Linux-x86_64.sh`
	- press enter a bunch of times then enter 'yes'
	- `source ~/.bashrc`
4. cd into this folder (CichlidBowerTracking/cichlid_bower_tracking/deeplabcut_setup)
5. conda env create -f DEEPLABCUT.yaml
6. conda install -c conda-forge cudnn
7. find the path to your conda environment
	- if you installed miniconda @ your root it should be something like "/data/home/<username>/miniconda3/envs/DEEPLABCUT"
8. execute: `nano ~/.bashrc`
9. add the following line to the ~/.bashrc file 
	- export PATH=/data/home/<username>/miniconda3/envs/DEEPLABCUT/bin:$PATH
10. Ctrl+O to save the ~/.bashrc file, Ctrl+X to exit
11. execute: ``source ~/.bashrc`
12. to check if you have deeplabcut properly installed
	- open a python terminal by typing `python` and pressing enter
	- in the python terminal `import deeplabcut`
	- it will give some warnings, but it should say 'DLC loaded in light mode; you cannot use any GUI...' with no error messages after
	- now you can train a model!