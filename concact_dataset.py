import json
import os
from tqdm import tqdm

meta_data_folder="./meta_data_subset"


for i in tqdm(range(1, 6)):
    meta_data = []
    postfix = f"_{i}.json"
    # 将所有以postfix结尾的文件拼接为一个json文件
    for file in os.listdir(meta_data_folder):
        if file.endswith(postfix) and not file.startswith("all"):
            with open(os.path.join(meta_data_folder, file), "r") as f:
                meta_data.extend(json.load(f))

    with open(os.path.join(meta_data_folder, f"all{postfix}"), "w") as f:
        json.dump(meta_data, f, indent=4)

    print(f"{i} done")