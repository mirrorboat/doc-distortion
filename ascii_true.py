import json

source="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/all_add_image_path_prefix_add_mineru_image_token_and_ocr_with_format.json"
target="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset/all_add_image_path_prefix_add_mineru_image_token_and_ocr_with_format_ascii_false.json"
# 读取source文件，该文件在保存时设置了ensure_ascii=True，下面另存为时设置ensure_ascii=False
with open(source, 'r') as f:
    data = json.load(f)

# 保存时设置ensure_ascii=False
with open(target, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)