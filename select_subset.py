# data = {'mineru_cn1M':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn1M.json',
#     },
#     'mineru_en1M':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en1M.json'
#     },
#     'mineru_cn2M':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn2M.json',
#     }, # 300k * 2
#     'mineru_en2M':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en2M.json'
#     }, # 300k * 2
#     'table_cn440K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_zh440K.json'
#     }, # 100k * 2
#     'table_en100K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_en100K.json'
#     }, # 50k * 2
#     'exam_cn140K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#         'annotations':'/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_zh140K.json'
#     }, # 140k
#     'exam_en8K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_en8K.json'
#     }, # 8k
#     '3col_cn30K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_zh30K.json'
#     }, # 30k
#     '3col_en20K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_en20K.json'
#     }, # 20k
#     'newspaper_cn60K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/newpaper_zh-700-K/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_newspaper_zh60K.json'
#     },
#     'numinamath_30w':{
#         'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot/',
#         'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot.json',
#     }, 
#     'openmath_40w':{
#         'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2/',
#         'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2.json',
#     },} # 10w(100k) * 2


# data = {
#     'mineru_cn2M': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_cn-2000k.json",
#     'mineru_en2M': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_en-2000k.json",
#     'table_cn440K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_table_zh-440k.json",
#     'table_en100K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_table_en-100k.json",
#     'exam_cn140K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_exam_zh-140k.json",
#     'exam_en8K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_exam_en-8k.json",
#     '3col_cn30K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_3col_zh-30k.json",
#     '3col_en20K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_3col_en-20k.json",
#     'newspaper_cn60K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_newspaper_zh-60k.json",
#     'math_cn200K': "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru_lvlm_data/mineru_math_cn200K.json",
#     'math_en200K': "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru_lvlm_data/mineru_math_en200K.json",
# }

# # 逐个打印json文件的长度
# import json

# for key, value in data.items():
#     with open(value['annotations'], 'r') as f:
#         meta_data = json.load(f)
#     print(key, len(meta_data))


# mineru_cn1M 1006510
# mineru_en1M 1001864
# mineru_cn2M 2005084
# mineru_en2M 2001529
# table_cn440K 440960
# table_en100K 99647
# exam_cn140K 143663
# exam_en8K 8302
# 3col_cn30K 29781
# 3col_en20K 23518
# newspaper_cn60K 65518
# numinamath_30w 335209
# openmath_40w 398449

import random
import os

# data={
#     'mineru_cn2M':
#     {
#         'total_num': 2005084,
#         'subset_num': 80000,
#     },
#     'mineru_en2M':
#     {
#         'total_num': 2001529,
#         'subset_num': 80000,
#     },
#     'table_cn440K':{
#         'total_num': 440960,
#         'subset_num': 10000,
#     },
#     'table_en100K':{
#         'total_num': 99647,
#         'subset_num': 6000,
#     },
#     'exam_cn140K':{
#         'total_num': 143663,
#         'subset_num': 10000,
#     },
#     # 'exam_en8K':{
#     #     'total_num': 8302,
#     #     'subset_num': 1600,
#     # }, # 数据用尽
#     '3col_cn30K':{
#         'total_num': 29781,
#         'subset_num': 2000,
#     },
#     '3col_en20K':{
#         'total_num': 23518,
#         'subset_num': 2000,
#     },
#     # 'openmath_40w':{
#     #     'total_num': 398449,
#     #     'subset_num': 10000,
#     # }, # 旧版数据不再使用
#     "math_cn200K": {
#         'total_num': 191794,
#         'subset_num': 10000,
#     },
#     "math_en200K": {
#         'total_num': 200812,
#         'subset_num': 10000,
#     },
# }

data={
    # 'table_en100K':{
    #     'total_num': 99647,
    #     'subset_num': 6000,
    # },
    'newspaper_cn60K':{
        'total_num': 65518,
        'subset_num': 2000,
    },
}

# 第一次采样：
# for key, value in data.items():
#     print(key)
#     idxs = random.sample(range(value['total_num']), value['subset_num']*5)
#     # idxs.sort()
#     folder = "./subset_idx"
#     # 将idxs分成5份，分别存储
#     for i in range(5):
#         path = f"{key}_{value['subset_num']}_{i+1}.txt"
#         if not os.path.exists(folder):
#             os.makedirs(folder)
#         with open(os.path.join(folder, path), "w") as f:
#             idx_subset = idxs[i*value['subset_num']:(i+1)*value['subset_num']]
#             idx_subset.sort()
#             for idx in idx_subset:
#                 f.write(str(idx) + "\n")

# # 再次采样mineru_cn2M和mineru_en2M，要求不得重复采样第一次的样本，因此需要先读取第一次的idx，将其从候选idx中去除
# folder = "./subset_idx"

# for key, value in data.items():
#     if key in ['mineru_cn2M', 'mineru_en2M']:
#         print(key)
#         old_idxs = []
#         for i in range(5):
#             path = f"{key}_{value['subset_num']}_{i+1}.txt"
#             with open(os.path.join(folder, path), "r") as f:
#                 old_idxs.extend([int(idx) for idx in f.readlines()])
#         candidate_idx= set(range(value['total_num'])) - set(old_idxs)
#         candidate_idx = list(candidate_idx)
#         idxs = random.sample(candidate_idx, 150000)
#         idxs.sort()
#         path = f"{key}_150000_5_new.txt"
#         with open(os.path.join(folder, path), "w") as f:
#             for idx in idxs:
#                 f.write(str(idx) + "\n")



# 依据data进行第三次采样，要求不得重复采样第一次和第二次的样本，因此需要先读取第一次和第二次的idx，将其从候选idx中去除
folder = "./subset_idx"

for key, value in data.items():
    print(f"****{key}***")
    old_idxs = []
    if key not in ['math_cn200K', 'math_en200K', 'newspaper_cn60K']:
        for i in range(5):
            # path = f"{key}_{value['subset_num']}_{i+1}.txt"
            # 在folder下寻找以{key}开头，以_{i+1}.txt结尾的文件作为path:
            path = [f for f in os.listdir(folder) if f.startswith(key) and f.endswith(f"_{i+1}.txt")][0]
            print(path)
            with open(os.path.join(folder, path), "r") as f:
                old_idxs.extend([int(idx) for idx in f.readlines()])

        if key in ['mineru_cn2M', 'mineru_en2M']:
            path = f"{key}_150000_5_new.txt"
            with open(os.path.join(folder, path), "r") as f:
                old_idxs.extend([int(idx) for idx in f.readlines()])

    print(f"old_idxs: {len(old_idxs)}")
    candidate_idx= set(range(value['total_num'])) - set(old_idxs)
    candidate_idx = list(candidate_idx)
    if len(candidate_idx) < value['subset_num']*6:
        print(f"not enough candidate idx for {key}")
        continue
    idxs = random.sample(candidate_idx, value['subset_num']*6) # 多出来的一份用于无失真数据
    idxs.sort()

    for i in range(5):
        if i == 4:
            path = f"{key}_{value['subset_num']*2}_{i+1}_third_sampling.txt"
        else:
            path = f"{key}_{value['subset_num']}_{i+1}_third_sampling.txt"
        with open(os.path.join(folder, path), "w") as f:
            if i == 4:
                idx_subset = idxs[i*value['subset_num']:] # i=4（无失真数据）数据量是其他数据的2倍
            else:
                idx_subset = idxs[i*value['subset_num']:(i+1)*value['subset_num']]

            idx_subset.sort()
            for idx in idx_subset:
                f.write(str(idx) + "\n")
