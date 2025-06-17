from s3_utils import get_s3_client, read_s3_object, read_s3_object_content
import os
import random
import cv2
import numpy as np

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

path = "s3://xyz-process-huawei/nlp/xyz_unified_format/cc-open-release-delivery/v004/ar/culture/common_crawl/train-677e0db8a461-000100.bin.meta"

s3_bucket_name = "doc-parse-huawei"
s3_prefix = "mineru2/synthdog/coco_img/train2017.zip"
local_folder_path = "/mnt/petrelfs/chenjingzhou/cjz/opendatalab/cjz/coco/train2017.zip"   # Local folder path to save the files


s3_client.download_file(s3_bucket_name, s3_prefix, local_folder_path)