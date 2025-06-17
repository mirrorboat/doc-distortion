import cv2
import numpy as np
import os
import random
from augraphy import *
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed


class doc_distortion():
    def distortion(self, image):
        pass

    def __call__(self, image):
        if hasattr(self, "image_size_threshold"):
            original_height, original_width = image.shape[:2]
            if original_height > original_width and original_height > self.image_size_threshold:
                image = cv2.resize(image, (self.image_size_threshold, int(self.image_size_threshold*original_width/original_height)))
            elif original_width > original_height and original_width > self.image_size_threshold:
                image = cv2.resize(image, (int(self.image_size_threshold*original_height/original_width), self.image_size_threshold))

        augmented_image = self.distortion(image)

        if hasattr(self, "image_size_threshold"):
            augmented_image = cv2.resize(augmented_image, (original_width, original_height))

        return augmented_image


class blur(doc_distortion):
    def __init__(self, psf_folder, psf_size_mode="interval", ratio_interval = (0.015, 0.025), image_size_threshold=1500):
        psf_paths = os.listdir(psf_folder)
        psf_paths = [os.path.join(psf_folder, psf_path) for psf_path in psf_paths]
        self.psf_list = [self.read_psf(psf_path) for psf_path in psf_paths]
        self.psf_size_mode = psf_size_mode
        self.image_size_threshold = image_size_threshold
        self.ratio_interval = ratio_interval # the bigger the ratio, the bigger the psf size

    def read_psf(self, psf_path):
        psf = cv2.imread(psf_path, cv2.IMREAD_GRAYSCALE)
        if psf.shape[0] % 2 == 0 or psf.shape[1] % 2 == 0:
            raise ValueError("PSF image dimensions must be odd.")
        # psf = psf / np.sum(psf)
        return psf
    
    def distortion(self, image):
        idx = random.randint(0, len(self.psf_list)-1)
        psf = self.psf_list[idx]

        image_size = min(image.shape[:2])
        image_size = min(image_size, self.image_size_threshold)

        if self.psf_size_mode == "interval":
            if image_size < 600:
                psf_size = 7
            elif image_size < 800:
                psf_size = 9
            else:
                psf_size = 11
        elif self.psf_size_mode == "ratio":
            ratio = random.uniform(*self.ratio_interval)
            psf_size = int(image_size * ratio)
            if psf_size % 2 == 0:
                psf_size += 1
            # print(f"psf_size: {psf_size}")
        else:
            raise ValueError("psf_size_mode must be either 'interval' or 'ratio'.")

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

class shadow(doc_distortion):
    def __init__(self, ink_color_range=(-1, -1)):
        self.ink_color_range = ink_color_range
        self.ink_phase = []
        self.paper_phase = []
        self.post_phase = [
            LightingGradient(
                light_position=None,
                direction=None,
                max_brightness=255,
                min_brightness=0,
                mode="gaussian",
                linear_decay_rate=None,
                transparency=None,
            ),
            ShadowCast(
                shadow_vertices_range=(4,8),
                shadow_opacity_range = (0.7, 0.9),
                shadow_width_range=(0.8, 1.0),
                shadow_height_range=(0.8, 1.0),
                p=1,
            ),
        ]
        self.pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase, ink_color_range=self.ink_color_range)

    def distortion(self, image):
        augmented_image = self.pipeline(image)
        return augmented_image
    
class wrap(doc_distortion):
    def __init__(self, ink_color_range=(-1, -1)):
        self.ink_color_range = ink_color_range

    def distortion(self, image):
        ink_phase = []
        paper_phase = []
        post_phase = [
            Geometric(
                rotate_range = random.choice([(-30, -5), (5, 30)]),
                p=0.9,
            ),
            Folding(
                fold_x=None,
                fold_deviation=(0, 0),
                fold_angle_range=(-180, 180),
                fold_count=random.randint(8, 10),
                fold_noise=random.uniform(0, 0.15),
                gradient_width=(0.1, 0.2),
                gradient_height=(0.01, 0.02),
            ),
        ]
        self.pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, ink_color_range=self.ink_color_range)

        augmented_image = self.pipeline(image)
        return augmented_image
    
class binarization(doc_distortion):
    def __init__(self, ink_color_range=(-1, -1)):
        self.ink_color_range = ink_color_range

    def distortion(self, image):
        ink_phase = [
            OneOf(
                [
                    InkBleed(
                        intensity_range=(0.5, 0.6),
                        kernel_size=random.choice([(5, 5), (3, 3)]),
                        severity=(0.5, 0.6),
                    ),
                    Letterpress(
                        n_samples=(100, 400),
                        n_clusters=(200, 400),
                        std_range=(500, 3000),
                        value_range=(150, 224),
                        value_threshold_range=(96, 128),
                        blur=1,
                    ),
                ],
            ),
        ]

        paper_phase = [
            PatternGenerator(
                imgx=random.randint(256, 512),
                imgy=random.randint(256, 512),
                n_rotation_range=(10, 15),
                color="random",
                alpha_range=(0.4, 0.4),
            ),

            BleedThrough(
                intensity_range=(0.6, 0.9),
                color_range=(0, 224),
                ksize=(17, 17),
                sigmaX=1,
                alpha=random.uniform(0.2, 0.3),
                offsets=(10, 20),
            ),
        ]

        post_phase = [
            Markup(
                num_lines_range=(15, 20),
                markup_length_range=(0.8, 1),
                markup_thickness_range=(2, 3),
                markup_type="highlight",
            ),
        ]

        pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, ink_color_range=self.ink_color_range)
        augmented_image = pipeline(image)
        return augmented_image