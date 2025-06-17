import json
import os
from tqdm import tqdm 
chunk_num=16
distortion_ls=["binarization", "blur", "warp", "shadow"]

# folder="0403distortion_note"
for distortion in distortion_ls:
    combined_data=[]
    for chunk_idx in tqdm(range(chunk_num)):
        path=f"mineru2_notes_{distortion}_{chunk_idx:02d}_{chunk_num:02d}.json"
        # path=os.path.join(folder, path)
        with open(path, 'r') as f:
            meta_data = json.load(f)
        # 将数据合并到combined_data
        combined_data.extend(meta_data)

    # 将合并后的数据保存到文件
    combined_path=f"mineru2_notes_{distortion}_combined_{len(combined_data)}.json"
    # combined_path=os.path.join(folder, combined_path)
    with open(combined_path, 'w') as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)
