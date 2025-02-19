from PIL import Image
import random
import os
from tqdm import tqdm

# 按照三度递增
rotate_angle = [i for i in range(5, 35, 5)]
# print(rotate_angle)
input_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/GT"

def rotate_image(input_path, angle):
    angle = angle * random.choice([-1, 1])
    with Image.open(input_path) as img:
        rotated_img = img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    return rotated_img

for angle in tqdm(rotate_angle):
    output_folder=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/rotate-{angle:02d}"

    # 遍历input_folder下的所有图片，包括子文件夹下的图片，使用rotate_image函数对每张图片进行旋转，然后以相同的文件结构保存到output_folder下

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            output_path = input_path.replace(input_folder, output_folder)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            rotated_img = rotate_image(input_path, angle)
            rotated_img.save(output_path)
            # print(input_path, output_path)

