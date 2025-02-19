import json
import os
from tqdm import tqdm

meta_data_folder="./meta_data_subset"

prefix="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images2"

id_2_distortion={
    1: "binarization",
    2: "blur",
    3: "shadow",
    4: "wrap",
    5: "none",
}

for i in range(1, 6):
    count=0
    new_mata_data=[]
    with open(os.path.join(meta_data_folder, f"all_{i}.json"), "r") as f:
        meta_data = json.load(f)
    for data in tqdm(meta_data):
        if os.path.exists(os.path.join(prefix, id_2_distortion[i], data["image"])):
            new_data={
                "query": data["conversations"][0]["value"],
                "response": data["conversations"][1]["value"],
                "images": [os.path.join(prefix, id_2_distortion[i], data["image"])]
            }
            # data["image"] = os.path.join(prefix, id_2_distortion[i], data["image"])
            new_mata_data.append(new_data)
        else:
            count+=1
    with open(os.path.join(meta_data_folder, f"all_add_image_path_prefix_{i}.json"), "w") as f:
        json.dump(new_mata_data, f, indent=4)
    print(count)


print("done")