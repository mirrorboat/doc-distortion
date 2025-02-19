from s3_utils import get_s3_client, read_s3_object, read_s3_object_content
import os
import random
from torch.utils.data import Dataset
import json
import cv2
import numpy as np

class s3Dataset(Dataset):
    def __init__(self, meta_data, folder):
        self.init_client()
        self.meta_data = meta_data
        self.folder = folder

    def init_client(self):
        # 10.140.96.129 ~ 10.140.96.164
        ip_idx = random.choice(range(164-129)) + 129
        
        s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
        self.s3_client = get_s3_client("", s3_load_cfg_huawei)

    def __len__(self):
        return len(self.meta_data)

    def __getitem__(self, idx):
        # return self.meta_data[idx]["image"].split("/")[-1], read_s3_object_content(self.s3_client, os.path.join(self.folder, self.meta_data[idx]["image"]))
        # return self.meta_data[idx]["image"], read_s3_object_content(self.s3_client, os.path.join(self.folder, self.meta_data[idx]["image"]))
        # 返回的图像应为cv2格式的图像而非bytes
        return self.meta_data[idx]["image"], cv2.imdecode(np.frombuffer(read_s3_object_content(self.s3_client, os.path.join(self.folder, self.meta_data[idx]["image"])), np.uint8), cv2.IMREAD_COLOR)

class localDataset(Dataset):
    def __init__(self, meta_data, folder):
        self.meta_data = meta_data
        self.folder = folder

    def __len__(self):
        return len(self.meta_data)

    def __getitem__(self, idx):
        # with open(os.path.join(self.folder, self.meta_data[idx]["image"]), "rb") as f:
        #     return self.meta_data[idx]["image"], f.read()
        return self.meta_data[idx]["image"], cv2.imread(os.path.join(self.folder, self.meta_data[idx]["image"]))