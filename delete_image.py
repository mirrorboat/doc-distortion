import json
import os
from tqdm import tqdm

json_ls = [
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_1_bigger_distortion.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_2_bigger_distortion.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_3_bigger_distortion.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_4_bigger_distortion.json"
]

# 删除"image"字段所指定路径的文件
for json_file_path in json_ls:
    with open(json_file_path, "r") as f:
        data = json.load(f)
    for item in tqdm(data):
        image_path = item.get("image")
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            # print(f"Deleted {image_path}")
        else:
            print(f"Skipping invalid image_path: {image_path}")