import json
from tqdm import tqdm

old_prefix="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/"
new_prefix="s3://doc-parse-huawei/test_jingzhou/distortion/"
for idx in tqdm(range(1, 5)):
    # all_data=[]

    path=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_{idx}_bigger_distortion.json"
    with open(path, 'r') as f:
        meta_data = json.load(f)
    for i in range(len(meta_data)):
        meta_data[i]["image"] = meta_data[i]["image"].replace(old_prefix, new_prefix)
    # all_data.extend(meta_data)

    new_path=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_{idx}_bigger_distortion_new_path_{len(meta_data)}.json"

    with open(new_path, 'w') as f:
        json.dump(meta_data, f, indent=4, ensure_ascii=False)
