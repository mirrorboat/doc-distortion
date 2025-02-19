# import json
# import random

# path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/all_add_image_path_prefix_add_mineru_image_token_and_ocr_with_format.json"

# # 随机选取四分之一的数据并保存

# with open(path, "r") as f:
#     meta_data = json.load(f)
#     meta_data = random.sample(meta_data, len(meta_data))
#     meta_data = meta_data[:int(len(meta_data)/4)]
#     print(len(meta_data))

# print(meta_data[:5])

# with open("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/all_add_image_path_prefix_add_mineru_image_token_and_ocr_with_format_1_4.json", "w") as f:
#     json.dump(meta_data, f, indent=4)

import json
path="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/mineru_cn2M_1.json"

with open(path, "r") as f:
    meta_data = json.load(f)
    print(meta_data[:5])