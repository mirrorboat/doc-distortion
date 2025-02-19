import json
import os
from tqdm import tqdm
import random

path="./meta_data_subset/all_add_image_path_prefix_add_mineru_image_token.json"

with open(path, "r") as f:
    meta_data = json.load(f)
    for i in tqdm(range(len(meta_data))):
        meta_data[i]["conversations"][0]["value"]+="OCR with format: "
        if i == 0:
            print(meta_data[i]["conversations"][0]["value"])

random.shuffle(meta_data)

with open("./meta_data_subset/all_add_image_path_prefix_add_mineru_image_token_and_ocr_with_format.json", "w") as f:
    json.dump(meta_data, f, indent=4)
