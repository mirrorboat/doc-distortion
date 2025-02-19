import json
import os

# meta_data_prefix="./meta_data_subset/all_add_image_path_prefix_"

# # combine the file
# length=0
# combined_meta_data=[]
# for i in range(1, 6):
#     with open(meta_data_prefix+f"{i}.json", "r") as f:
#         meta_data = json.load(f)
#         print(len(meta_data))
#         length+=len(meta_data)
#     # combined_meta_data+=meta_data

# print(length)
# # with open(meta_data_prefix+"combined.json", "w") as f:
# #     json.dump(combined_meta_data, f, indent=4)

with open("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/all_add_image_path_prefix_combined.json", "r") as f:
    meta_data = json.load(f)
    print(len(meta_data))
