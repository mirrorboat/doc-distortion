import random
from augraphy import *
import cv2
import os

ink_phase = [
    # # BleedThrough(),
    # BleedThrough(
    #     intensity_range=(0.1, 0.9),
    #     color_range=(0, 224),
    #     ksize=(17, 17),
    #     sigmaX=1,
    #     alpha=random.uniform(0.9, 1.2),
    #     offsets=(10, 20),
    #     p=1,
    # ),
]


paper_phase = [
]

post_phase = [
]

input_folder="./input/GT/EN"
output_folder="./testset/EN"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# 遍历input_folder，处理其中的所有图片，然后保存到output_folder
for i, filename in enumerate(os.listdir(input_folder)):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        input_path=os.path.join(input_folder, filename)
        image = cv2.imread(input_path)
        pipeline = AugraphyPipeline(ink_phase=ink_phase, 
                                    paper_phase=paper_phase, 
                                    post_phase=post_phase, 
                                    overlay_alpha=0.1)
        augmented_image=pipeline(image)
        cv2.imwrite(f"{output_folder}/{filename}",augmented_image)
