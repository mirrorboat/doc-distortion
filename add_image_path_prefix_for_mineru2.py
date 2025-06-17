import json
import os
from tqdm import tqdm
import random
from PIL import Image

id_2_distortion={
    1: "binarization",
    2: "blur",
    3: "shadow",
    4: "wrap",
    5: "none",
}

meta_data_folder="./meta_data_subset_third_sampling"

old_prefix="mineru:s3://doc-parse-huawei/"
new_prefix="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images3"

for i in range(2, 6):
    new_mata_data=[]
    count=0
    with open(os.path.join(meta_data_folder, f"all_{i}.json"), "r") as f:
        meta_data = json.load(f)
    for data in tqdm(meta_data):
        # image_path=os.path.join(prefix, id_2_distortion[i], data["image"])
        # delete the old_prefix 
        image_path=data["image"].removeprefix(old_prefix)
        image_path=os.path.join(new_prefix, id_2_distortion[i], image_path)
        # print(image_path)
        # exit()
        if os.path.exists(image_path):
            # 尝试读取图片，以避免图像文件不完整
            try:
                img = Image.open(image_path)
            except:
                print(f"read error: {image_path}")
                continue
            data["image"]=image_path
            new_mata_data.append(data)
        else:
            print(image_path, flush=True)
            # exit()
            count+=1

    print(count)

    random.shuffle(new_mata_data)

    with open(os.path.join(meta_data_folder, f"all_{i}_old_distortion.json"), "w") as f:
        print(f"***len: {len(new_mata_data)}")
        json.dump(new_mata_data, f, indent=4, ensure_ascii=False)
    print(f"{i} done")