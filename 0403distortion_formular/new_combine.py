import json
import os
import random
# 将所有文件名中含有0430的json文件合并

file_ls = os.listdir("./")
file_ls = [file for file in file_ls if "0430" in file and file.endswith(".json")]
combined_data = []

for file in file_ls:
    with open(file, 'r') as f:
        meta_data = json.load(f)
    # 将数据合并到combined_data
    combined_data.extend(meta_data)

# shuffle combined_data
random.shuffle(combined_data)

# 将合并后的数据保存到文件
combined_path = f"0430_combined_{len(combined_data)}.json"
print(combined_path)
with open(combined_path, 'w') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)