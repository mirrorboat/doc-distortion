import json
import os
from tqdm import tqdm

# meta_data_folders=["./meta_data_subset_first_second_sampling", "./meta_data_subset_third_sampling"]
# meta_data_folders=["./meta_data_subset_third_sampling"]
meta_data_folders=["./meta_data_subset_first_second_sampling"]


for i in tqdm(range(1, 6)):
    # postfix = (f"_{i}.json", f"_{i}_third_sampling.json")
    postfix = (f"_{i}.json")
    # 将所有以postfix结尾的文件拼接为一个json文件
    for meta_data_folder in meta_data_folders:
        meta_data = []
        for file in os.listdir(meta_data_folder):
            if file.endswith(postfix) and not file.startswith("all"):
                print(file)
                with open(os.path.join(meta_data_folder, file), "r") as f:
                    meta_data.extend(json.load(f))

        with open(os.path.join(meta_data_folder, f"all_{i}.json"), "w") as f:
            json.dump(meta_data, f, indent=4)

    print(f"{i} done", flush=True)