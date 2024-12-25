import cv2
import numpy as np
import os
import random

HEIGHT_THRESHOLD = 1500

def read_psf(psf_path):
    psf_image = cv2.imread(psf_path, cv2.IMREAD_GRAYSCALE)
    if psf_image.shape[0] % 2 == 0 or psf_image.shape[1] % 2 == 0:
        raise ValueError("PSF image dimensions must be odd.")
    psf = psf_image / np.sum(psf_image)
    return psf

def psf_blur(image, psf):
    b, g, r = cv2.split(image)
    blurred_b = cv2.filter2D(b, -1, psf)
    blurred_g = cv2.filter2D(g, -1, psf)
    blurred_r = cv2.filter2D(r, -1, psf)
    blurred_image = cv2.merge((blurred_b, blurred_g, blurred_r))
    return blurred_image

psf_folder="./psf"
psf_paths = random.sample(os.listdir(psf_folder), 100)
psf_paths = [os.path.join(psf_folder, psf_path) for psf_path in psf_paths]
print(psf_paths)

input_folder="./input/GT/"
output_folder="./testset/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
for idx, filename in enumerate(os.listdir(input_folder)):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        input_path=os.path.join(input_folder, filename)
        image = cv2.imread(input_path)
        height=0
        weight=0
        if image.shape[0]>HEIGHT_THRESHOLD:
            height=image.shape[0]
            weight=image.shape[1]
            image = cv2.resize(image, (HEIGHT_THRESHOLD, int(HEIGHT_THRESHOLD*image.shape[1]/image.shape[0])))
            
        psf= read_psf(psf_paths[idx])
        augmented_image=psf_blur(image, psf)
        if height>0:
            augmented_image = cv2.resize(augmented_image, (weight, height))
        cv2.imwrite(f"{output_folder}/{filename}",augmented_image)