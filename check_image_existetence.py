import json
import os
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--distortion", type=str, required=True)
args = parser.parse_args()
distortion_2_postfix={
    'binarization': 1,
    'blur': 2,
    'shadow': 3,
    'wrap': 4,
    'none': 5,
}

data_name=["mineru_cn2M", "mineru_en2M", "table_cn440K", "table_en100K", "exam_cn140K", "exam_en8K", "3col_cn30K", "3col_en20K", "openmath_40w"]


error_folder = "./none_existence_data"
error_file = os.path.join(error_folder, args.distortion+".txt")
if os.path.exists(error_file):
    os.remove(error_file)
for name in data_name:
    data_folder="./meta_data_subset"
    distortion = args.distortion
    data_path=name+"_"+str(distortion_2_postfix[distortion])+".json"
    print(data_path)
    image_folder="./batch_distorted_images2"

    with open(os.path.join(data_folder, data_path), "r") as f:
        meta_data_dict_ls = json.load(f)

    error_list = []
    for meta_data in tqdm(meta_data_dict_ls):
        if not os.path.exists(os.path.join(image_folder, distortion,  meta_data["image"])):
            error_list.append(os.path.join(image_folder, distortion, meta_data["image"]))

    if not os.path.exists(error_folder):
        os.makedirs(error_folder)

    with open(error_file, "a") as f:
        f.write(f"*********data: {name}*********\n")
        f.write(f"error num: {len(error_list)}\n")
        for error in error_list:
            f.write(error + "\n")
    print(f"{data_path} done")
    