import json
import os
import random
# from s3_utils import get_s3_client, read_s3_object_content

# sourse="/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en1M.json"
# with open(sourse, 'r') as f:
#     meta_data = json.load(f)

# meta_data = meta_data[:16]
# target="./target.json"
# with open(target, 'w') as f:
#     json.dump(meta_data, f)


from data_utils import s3Dataset

with open("./target.json", 'r') as f:
    meta_data = json.load(f)
image_folder='s3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/'

dataset = s3Dataset(meta_data, image_folder)
target_folder = "images"
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
print("start downloading")
# 开始记时
import time
start = time.time()
for idx in range(len(dataset)):
    image_name, image = dataset[idx]
    # 判断os.path.join(target_folder, image_name)对应的文件夹是否存在，不存在则创建
    if not os.path.exists(os.path.dirname(os.path.join(target_folder, image_name))):
        os.makedirs(os.path.dirname(os.path.join(target_folder, image_name)))
    with open(os.path.join(target_folder, image_name), "wb") as f:
        f.write(image)
end = time.time()
print(f"下载完成，耗时{end-start}秒")

# ip_idx = random.choice(range(164-129)) + 129
# s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
# s3_client = get_s3_client("", s3_load_cfg_huawei)

# for idx in range(16):
#     read_s3_object_content(s3_client, os.path.join(folder, meta_data[idx]["image"]))
#     # 存到./images文件夹
#     with open(os.path.join("./images", meta_data[idx]["image"]), "wb") as f:
#         f.write(read_s3_object_content(s3_client, os.path.join(folder, meta_data[idx]["image"])))
