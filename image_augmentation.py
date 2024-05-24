from PIL import Image, ImageEnhance
import numpy as np
import os
import random
import argparse

"""
Image Augmentation Script

This script performs data augmentation on a dataset of images by applying random color transformations and 
optionally converting the images to grayscale. The purpose is to enhance the dataset for training neural networks, 
ensuring that the network does not rely on the color of the images to make predictions.

Usage:
    python image_augmentation.py input_folder output_folder --num_augmentations 5 --include_grayscale

Arguments:
    input_folder (str): Path to the input folder containing images.
    output_folder (str): Path to the output folder to save augmented images.
    --num_augmentations (int): Number of augmentations to perform per image (default is 5).
    --include_grayscale (flag): Include grayscale conversion of images if set.

Functions:
    parse_args(): Parses command-line arguments.
    random_color_augmentation(image): Applies random color transformations to an image.
    convert_to_grayscale(image): Converts an image to grayscale.
    augment_dataset(input_folder, output_folder, num_augmentations=5, include_grayscale=False): 
        Augments the dataset with color transformations and optionally includes grayscale images.
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Augment image dataset with color transformations and optional grayscale conversion.")
    parser.add_argument('input_folder', type=str, help="Path to the input folder containing images.")
    parser.add_argument('output_folder', type=str, help="Path to the output folder to save augmented images.")
    parser.add_argument('--num_augmentations', type=int, default=5, help="Number of augmentations to perform per image.")
    parser.add_argument('--include_grayscale', action='store_true', help="Include grayscale conversion of images.")
    return parser.parse_args()

def random_color_augmentation(image):
    # Convert the image to HSV (Hue, Saturation, Value)
    image = image.convert('HSV')
    np_img = np.array(image)

    # Randomly adjust hue
    hue_shift = np.random.randint(-30, 30)
    np_img[..., 0] = (np_img[..., 0] + hue_shift) % 256

    # Randomly adjust saturation
    sat_factor = 0.5 + np.random.random()
    np_img[..., 1] = np.clip(np_img[..., 1] * sat_factor, 0, 255)

    # Randomly adjust value (brightness)
    val_factor = 0.5 + np.random.random()
    np_img[..., 2] = np.clip(np_img[..., 2] * val_factor, 0, 255)

    # Convert back to RGB
    image = Image.fromarray(np_img, 'HSV').convert('RGB')

    return image

def augment_dataset(input_folder, output_folder, num_augmentations=5, include_grayscale=False):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            
            # Save original image
            image.save(os.path.join(output_folder, filename))
            
            # Generate augmented images
            for i in range(num_augmentations):
                augmented_image = random_color_augmentation(image)
                new_filename = f"{os.path.splitext(filename)[0]}_aug_{i}{os.path.splitext(filename)[1]}"
                augmented_image.save(os.path.join(output_folder, new_filename))
            
            # Optionally, convert the image to grayscale and save it
            if include_grayscale:
                grayscale_image = convert_to_grayscale(image)
                gray_filename = f"{os.path.splitext(filename)[0]}_gray{os.path.splitext(filename)[1]}"
                grayscale_image.save(os.path.join(output_folder, gray_filename))

if __name__ == '__main__':
    args = parse_args()
    augment_dataset(args.input_folder, args.output_folder, args.num_augmentations, args.include_grayscale)
