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
    
	`python image_augmentation.py input_folder output_folder --num_augmentations 5 --include_grayscale`

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
