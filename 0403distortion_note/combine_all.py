import json
import os
from tqdm import tqdm 
chunk_num=16
distortion_ls=["binarization", "blur", "warp", "shadow"]

# folder="0403distortion_note"
combined_data=[]

for distortion in distortion_ls:
    path=f"mineru2_notes_{distortion}_combined_50k.json"
    # path=os.path.join(folder, path)
    with open(path, 'r') as f:
        meta_data = json.load(f)
    # 将数据合并到combined_data
    combined_data.extend(meta_data)

# 将合并后的数据保存到文件
combined_path=f"mineru2_notes_distortion_combined_all_200k.json"
# combined_path=os.path.join(folder, combined_path)
with open(combined_path, 'w') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)
