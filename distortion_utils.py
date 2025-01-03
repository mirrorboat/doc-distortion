import cv2
import numpy as np
import os
import random
from augraphy import *

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
    def __init__(self, psf_folder, psf_size_ls=[9, 11, 13], image_size_threshold=1200):
        psf_paths = os.listdir(psf_folder)
        psf_paths = [os.path.join(psf_folder, psf_path) for psf_path in psf_paths]
        self.psf_list = [self.read_psf(psf_path) for psf_path in psf_paths]
        self.psf_size_ls = psf_size_ls
        self.image_size_threshold = image_size_threshold

    def read_psf(self, psf_path):
        psf_image = cv2.imread(psf_path, cv2.IMREAD_GRAYSCALE)
        if psf_image.shape[0] % 2 == 0 or psf_image.shape[1] % 2 == 0:
            raise ValueError("PSF image dimensions must be odd.")
        psf = psf_image / np.sum(psf_image)
        return psf
    
    def distortion(self, image):
        idx = random.randint(0, len(self.psf_list)-1)
        psf = self.psf_list[idx]
        psf_size = random.choice(self.psf_size)
        psf = cv2.resize(psf, (psf_size, psf_size))
        psf = cv2.rotate(psf, random.choice([cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]))

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
    def __init__(self):
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
                shadow_vertices_range=(5,10),
                shadow_opacity_range = (0.6, 0.8),
                shadow_width_range=(0.8, 1.0),
                shadow_height_range=(0.8, 1.0),
                p=1,
            ),
        ]
        self.pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase)

    def distortion(self, image):
        augmented_image = self.pipeline(image)
        return augmented_image
    
class wrap(doc_distortion):
    def __init__(self):
        self.ink_phase = []
        self.paper_phase = []
        self.post_phase = [
            Geometric(
                rotate_range=(-5, 5),
                p=0.2,
            ),
            Folding(
                fold_x=None,
                fold_deviation=(0, 0),
                fold_angle_range=random.choice([(0,0), (90,90),(45,45), (0, 90)]),
                fold_count=random.randint(2, 5),
                fold_noise=random.uniform(0, 0.15),
                gradient_width=(0.1, 0.2),
                gradient_height=(0.01, 0.02),
            ),
        ]
        self.pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase)

    def distortion(self, image):
        augmented_image = self.pipeline(image)
        return augmented_image
    
class binarization(doc_distortion):
    def __init__(self):
        self.ink_phase = [
            OneOf(
                [
                    BleedThrough(
                        intensity_range=(0.6, 0.9),
                        color_range=(0, 224),
                        ksize=(17, 17),
                        sigmaX=1,
                        alpha=random.uniform(0.2, 0.3),
                        offsets=(10, 20),
                    ),
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
                p=1.0
            ),
        ]

        self.paper_phase = [
            OneOf(
                [
                    DelaunayTessellation(
                        n_points_range=(500, 800),
                        n_horizontal_points_range=(500, 800),
                        n_vertical_points_range=(500, 800),
                        noise_type="random",
                        color_list="default",
                        color_list_alternate="default",
                    ),
                    PatternGenerator(
                        imgx=random.randint(256, 512),
                        imgy=random.randint(256, 512),
                        n_rotation_range=(10, 15),
                        color="random",
                        alpha_range=(0.15, 0.2),
                    ),
                    VoronoiTessellation(
                        mult_range=(50, 80),
                        seed=19829813472,
                        num_cells_range=(500, 1000),
                        noise_type="random",
                        background_value=(200, 255),
                    ),
                ],
            ),
        ]
        self.post_phase = []

    def distortion(self, image):
        pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase)
        augmented_image = pipeline(image)
        return augmented_image