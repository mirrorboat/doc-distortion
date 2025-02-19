# from PIL import Image
import cv2
import random
import os
from tqdm import tqdm
import numpy as np
import os

# ratio_ls = [0.01, 0.012, 0.015, 0.018]
# ratio_ls = [0.02, 0.022, 0.025]
ratio_ls = [0.02]
psf_folfer = "./psf_new"
# psf_subfolfer = ["line/small_line", "line/big_line", "circle/middle", "gaussian"]
psf_subfolfer = ["gaussian"]
input_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/GT"

class blur():
    def __init__(self, psf_folder, ratio = 0.01, image_size_threshold=1200):
        psf_paths = os.listdir(psf_folder)
        # print(psf_paths)
        # 只选取png和jpg格式的图片
        psf_paths = [psf_path for psf_path in psf_paths if psf_path.endswith(".png") or psf_path.endswith(".jpg")]
        psf_paths = [os.path.join(psf_folder, psf_path) for psf_path in psf_paths]
        self.psf_paths = psf_paths
        self.psf_list = [self.read_psf(psf_path) for psf_path in psf_paths]
        self.image_size_threshold = image_size_threshold
        self.ratio = ratio # the bigger the ratio, the bigger the psf size

    def read_psf(self, psf_path):
        psf = cv2.imread(psf_path, cv2.IMREAD_GRAYSCALE)
        if psf.shape[0] % 2 == 0 or psf.shape[1] % 2 == 0:
            raise ValueError("PSF image dimensions must be odd.")
        # psf = psf / np.sum(psf)
        return psf
    
    def distortion(self, image):
        idx = random.randint(0, len(self.psf_list)-1)
        print(f"psf_path: {self.psf_paths[idx]}", flush=True)
        psf = self.psf_list[idx]

        image_size = min(image.shape[:2])
        image_size = min(image_size, self.image_size_threshold)

        psf_size = int(image_size * self.ratio)
        if psf_size % 2 == 0:
            psf_size += 1
        print(f"psf_size: {psf_size}", flush=True)

        psf = cv2.resize(psf, (psf_size, psf_size))
        psf = cv2.rotate(psf, random.choice([cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]))
        psf = psf / np.sum(psf)

        if len(image.shape) < 3:
            blurred_image = cv2.filter2D(image, -1, psf)
        else:
            b, g, r = cv2.split(image)
            blurred_b = cv2.filter2D(b, -1, psf)
            blurred_g = cv2.filter2D(g, -1, psf)
            blurred_r = cv2.filter2D(r, -1, psf)
            blurred_image = cv2.merge((blurred_b, blurred_g, blurred_r))
        return blurred_image

    def __call__(self, image_path):
        image = cv2.imread(image_path)

        if self.image_size_threshold:
            original_height, original_width = image.shape[:2]
            if original_height > original_width and original_height > self.image_size_threshold:
                image = cv2.resize(image, (self.image_size_threshold, int(self.image_size_threshold*original_width/original_height)))
            elif original_width > original_height and original_width > self.image_size_threshold:
                image = cv2.resize(image, (int(self.image_size_threshold*original_height/original_width), self.image_size_threshold))

        augmented_image = self.distortion(image)

        if self.image_size_threshold:
            augmented_image = cv2.resize(augmented_image, (original_width, original_height))

        return augmented_image


for ratio in ratio_ls:
    for subfolder in psf_subfolfer:
        print(f"***start to process {subfolder}***")
        # blur_fn = blur("./psf", ratio, 1500)
        blur_fn = blur(os.path.join(psf_folfer, subfolder), ratio, 1500)
        subfolder_name = subfolder.replace("/", "-")
        output_folder=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/blur-{subfolder_name}-{ratio}"

        for root, dirs, files in os.walk(input_folder):
            for file in files:
                print(file, flush=True)
                input_path = os.path.join(root, file)
                output_path = input_path.replace(input_folder, output_folder)
                if not os.path.exists(os.path.dirname(output_path)):
                    os.makedirs(os.path.dirname(output_path))
                blur_image = blur_fn(input_path)
                cv2.imwrite(output_path, blur_image)
