import cv2
import numpy as np
import os
import random
from augraphy import *
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed


# def batch_distortion(distortion_fn, dataset):
#     # 使用多进程加速
#     pool = multiprocessing.Pool()
#     results = []
#     for image in dataset:
#         results.append(pool.apply_async(distortion_fn, args=(image,)))
    
#     pool.close()
#     pool.join()
#     augmented_images = [result.get() for result in results]
#     return augmented_images


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
    def __init__(self, psf_folder, ratio = 0.01, image_size_threshold=1200):
        psf_paths = os.listdir(psf_folder)
        psf_paths = [os.path.join(psf_folder, psf_path) for psf_path in psf_paths]
        self.psf_list = [self.read_psf(psf_path) for psf_path in psf_paths]
        # self.psf_size_ls = psf_size_ls
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
        psf = self.psf_list[idx]
        # psf_size = random.choice(self.psf_size_ls)

        image_size = min(image.shape[:2])
        image_size = min(image_size, self.image_size_threshold)

        # if image_size < 600:
        #     psf_size = 7
        # elif image_size < 800:
        #     psf_size = 9
        # else:
        #     psf_size = 11

        psf_size = int(image_size * self.ratio)
        if psf_size % 2 == 0:
            psf_size += 1
        print(f"psf_size: {psf_size}")

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
                shadow_vertices_range=(5,10),
                shadow_opacity_range = (0.4, 0.6),
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
        self.pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase, ink_color_range=self.ink_color_range)

    def distortion(self, image):
        augmented_image = self.pipeline(image)
        return augmented_image
    
class binarization(doc_distortion):
    def __init__(self, ink_color_range=(-1, -1)):
        self.ink_color_range = ink_color_range
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
        pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase, ink_color_range=self.ink_color_range)
        augmented_image = pipeline(image)
        return augmented_image
    

# def process_image(args):
#     """Helper function to apply distortion on a single image."""
#     idx, dataset, distortion_obj, target_folder = args
#     image_name, image_data = dataset[idx]
    
#     distorted_image = distortion_obj(image_data)
    
#     # with open(os.path.join(target_folder, image_name), "wb") as f:
#     #     f.write(distorted_image)

#     # with open(os.path.join("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/tmp/tmp.jpg"), "wb") as f:
#     #     f.write(distorted_image)
#     path=os.path.join(target_folder, image_name)
#     if not os.path.exists(os.path.dirname(path)):
#         os.makedirs(os.path.dirname(path))
#     cv2.imwrite(path, distorted_image)
        
#     return idx
#     # return distorted_image
#     # return os.path.join(target_folder, image_name)

# def parallel_distort_images(dataset, distortion_instance, target_folder, num_workers=None):
#     """
#     Applies doc_distortion in parallel using multiple processes.

#     Args:
#         dataset (s3Dataset): The dataset containing images.
#         distortion_instance (doc_distortion): An instance of the doc_distortion class.
#         num_workers (int, optional): Number of worker processes. Defaults to None, which uses all available CPU cores.

#     Returns:
#         list: A list of distorted images.
#     """
#     if num_workers is None:
#         num_workers = mp.cpu_count()

#     # distorted_images = []
#     results = []
#     with ProcessPoolExecutor(max_workers=num_workers) as executor:
#         futures = {executor.submit(process_image, (idx, dataset, distortion_instance, target_folder)) for idx in range(len(dataset))}
        
#         for future in as_completed(futures):
#             results.append(future.result())

#     return results