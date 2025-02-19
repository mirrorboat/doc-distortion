# from PIL import Image
import cv2
import random
import os
from augraphy import *
from tqdm import tqdm

# shadow_opacity = [0.5, 0.6, 0.7, 0.8]
shadow_opacity = [0.8]
input_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/GT"

def shadow(input_path, opacity):
    image = cv2.imread(input_path)
    ink_color_range = (0, 0)
    ink_phase = []
    paper_phase = []
    post_phase = [
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
            shadow_opacity_range = (opacity, opacity),
            shadow_width_range=(0.8, 1.0),
            shadow_height_range=(0.8, 1.0),
            p=1,
        ),
    ]
    pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, ink_color_range=ink_color_range)

    shadow_image = pipeline(image)

    return shadow_image

# for opacity in tqdm(shadow_opacity):
for opacity in shadow_opacity:
    output_folder=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/shadow-{opacity}"

    # 遍历input_folder下的所有图片，包括子文件夹下的图片，使用rotate_image函数对每张图片进行旋转，然后以相同的文件结构保存到output_folder下

    for root, dirs, files in os.walk(input_folder):
        for file in tqdm(files):
            input_path = os.path.join(root, file)
            output_path = input_path.replace(input_folder, output_folder)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            shadow_image = shadow(input_path, opacity)
            cv2.imwrite(output_path, shadow_image)
