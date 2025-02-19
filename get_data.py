from s3_utils import get_s3_client, read_s3_object, read_s3_object_content
import os
import random
# from torch.utils.data import Dataset
import json
from data_utils import s3Dataset, localDataset

# class s3Dataset(Dataset):
#     def __init__(self, meta_data, folder):
#         self.init_client()
#         self.meta_data = meta_data
#         self.folder = folder

#     def init_client(self):
#         # 10.140.96.129 ~ 10.140.96.164
#         ip_idx = random.choice(range(164-129)) + 129
        
#         s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
#         self.s3_client = get_s3_client("", s3_load_cfg_huawei)

#     def __len__(self):
#         return len(self.meta_data)

#     def __getitem__(self, idx):
#         return read_s3_object_content(self.s3_client, os.path.join(self.folder, self.meta_data[idx]["image"]))

# class localDataset(Dataset):
#     def __init__(self, meta_data, folder):
#         self.meta_data = meta_data
#         self.folder = folder

#     def __len__(self):
#         return len(self.meta_data)

#     def __getitem__(self, idx):
#         with open(os.path.join(self.folder, self.meta_data[idx]["image"]), "rb") as f:
#             return f.read()

# class subset(Dataset):
#     def __init__(self, dataset, idxs):
#         self.dataset = dataset
#         self.idxs = idxs
#         assert max(idxs) < len(dataset)

#     def __len__(self):
#         return len(self.idxs)

#     def __getitem__(self, idx):
#         return self.dataset[self.idxs[idx]]

data_dict = {'mineru_cn1M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn1M.json',
    },
    'mineru_en1M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en1M.json'
    },
    'mineru_cn2M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn2M.json',
    }, # 200k * 2
    'mineru_en2M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en2M.json'
    }, # 200k * 2
    'table_cn440K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_zh440K.json'
    }, # 220k * 2
    'table_en100K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_en100K.json'
    }, # 100k
    'exam_cn140K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations':'/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_zh140K.json'
    }, # 140k
    'exam_en8K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_en8K.json'
    }, # 8k
    '3col_cn30K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_zh30K.json'
    }, # 30k
    '3col_en20K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_en20K.json'
    }, # 20k
    'newspaper_cn60K':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/newpaper_zh-700-K/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_newspaper_zh60K.json'
    },
    'numinamath_30w':{
        'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot/',
        'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot.json',
    }, 
    'openmath_40w':{
        'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2/',
        'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2.json',
    },} # 10w(100k) * 4

if __name__ == "__main__":
    # image_folder = "s3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/"
    # meta_data_path = '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2.json'
    # with open(meta_data_path, 'r') as f:
    #     meta_data = json.load(f)
    # dataset = s3Dataset(meta_data, image_folder)
    # dataset = localDataset(meta_data, folder)


    for data_name, data_path in data_dict.items():
        print(data_name)
        # 依据data_name从subset_idx文件夹中读取对应的idxs,idxs文件的命名以data_name为前缀，后缀为"_1.txt"或"_2.txt",中间会有其他随机字符串，因此需要进行匹配
        idx_folder = "subset_idx"
        idxs1 = []
        for file in os.listdir(idx_folder):
            if file.startswith(data_name) and file.endswith("_1.txt"):
                with open(os.path.join(idx_folder, file), "r") as f:
                    idxs1 = [int(idx.strip()) for idx in f.readlines()]
        
        if len(idxs1) == 0:
            print(f"no idxs found for {data_name}")
            continue
        image_folder = data_path["images"]
        meta_data_path = data_path["annotations"]
        with open(meta_data_path, 'r') as f:
            meta_data = json.load(f)
        meta_data_subset = [meta_data[idx] for idx in idxs1]
        if image_folder.startswith("s3://"):
            dataset = s3Dataset(meta_data_subset, image_folder)
        else:
            dataset = localDataset(meta_data_subset, image_folder)
        # dataset_subset1 = subset(dataset, idxs1)
        # dataset_subset2 = subset(dataset, idxs2)

        

    # print(len(dataset))
    # sample_num = 400000
    # idxs = random.sample(range(len(dataset)), sample_num)
    # idxs1=idxs[:sample_num//2]
    # idxs2=idxs[sample_num//2:]
    # idx_folder="subset_idx"
    # # 将选取的400000个样本保存到本地txt，一行一个样本的index，文件名为meta_data_path的文件名加上"_400000"
    # with open(os.path.join(idx_folder, meta_data_path.split("/")[-1].split(".")[0] + "_200k_1.txt"), "w") as f:
    #     for idx in idxs1:
    #         f.write(str(idx) + "\n")
    # with open(os.path.join(idx_folder, meta_data_path.split("/")[-1].split(".")[0] + "_200k_2.txt"), "w") as f:
    #     for idx in idxs2:
    #         f.write(str(idx) + "\n")


    # # 随机选取10个样本保存到本地
    # target_folder = "3col_cn30K"
    # if not os.path.exists(target_folder):
    #     os.makedirs(target_folder)
    # for i in range(10):
    #     idx = random.choice(range(len(dataset)))
    #     image = dataset[idx]
    #     with open(os.path.join(target_folder, f"image_{idx}.jpg"), "wb") as f:
    #         f.write(image)