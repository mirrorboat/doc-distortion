import json
import os
from tqdm import tqdm
import random


meta_data_folder="./meta_data_subset"

prefix="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images2"

id_2_distortion={
    1: "binarization",
    2: "blur",
    3: "shadow",
    4: "wrap",
    5: "none",
}

new_mata_data=[]

# for i in range(1, 6):
#     count=0
#     with open(os.path.join(meta_data_folder, f"all_{i}.json"), "r") as f:
#         meta_data = json.load(f)
#     for data in tqdm(meta_data):
#         image_path=os.path.join(prefix, id_2_distortion[i], data["image"])
#         if os.path.exists(image_path):
#             data["image"]=image_path
#             # data["conversations"][0]["value"]="<Mineru-Image>\n"
#             data["conversations"][0]["value"]="<Mineru-Image>\nOCR with format: "
#             new_mata_data.append(data)
#         else:
#             count+=1

#     print(count)

# random.shuffle(new_mata_data)

datas = [
    "mineru_cn2M_5_new.json",
    "mineru_en2M_5_new.json"
]
for data_path in datas:
    count=0
    with open(os.path.join(meta_data_folder, data_path), "r") as f:
        meta_data = json.load(f)
    for data in tqdm(meta_data):
        image_path=os.path.join(prefix, "none", data["image"])
        if os.path.exists(image_path):
            data["image"]=image_path
            # data["conversations"][0]["value"]="<Mineru-Image>\n"
            data["conversations"][0]["value"]="<Mineru-Image>\nOCR with format: "
            new_mata_data.append(data)
        else:
            count+=1

    print(count)

random.shuffle(new_mata_data)

with open(os.path.join(meta_data_folder, f"0116_add_image_path_prefix_add_mineru_image_token.json"), "w") as f:
    json.dump(new_mata_data, f, indent=4, ensure_ascii=False)
print("done")