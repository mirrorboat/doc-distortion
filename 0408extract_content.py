import json
import re
import random
from tqdm import tqdm
def extract_and_join(text):
    # 定义正则表达式，匹配<|md_start|>和<|md_end|>之间的内容
    pattern = r'<\|md_start\|>(.*?)<\|md_end\|>'
    matches = re.findall(pattern, text, re.DOTALL)
    result = '\n\n'.join(matches)
    
    return result

metadata_ls=[
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/blur.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/binarization.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/shadow.json",
    "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/warp.json",
]

all_data=[]
for path in metadata_ls:
    with open(path, 'r') as f:
        metadata = json.load(f)
    if "shadow" in path or "blur" in path:
        # 使用random随机选择八万条
        print(path)
        metadata = random.sample(metadata, 70000)

    for data in tqdm(metadata):
        data["conversations"][1]["value"] = extract_and_join(data["conversations"][1]["value"])

    all_data.extend(metadata)

# 打乱all_data
random.shuffle(all_data)
new_path=f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/all_data_{len(all_data)}.json"
with open(new_path, 'w') as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

