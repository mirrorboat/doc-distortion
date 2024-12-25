import random
from augraphy import *
import cv2
import os

ink_phase = []

paper_phase = []

post_phase = [
    DepthSimulatedBlur(),
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
        pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)
        augmented_image=pipeline(image)
        cv2.imwrite(f"{output_folder}/{filename}",augmented_image)
