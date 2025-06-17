from distortion_utils import blur, shadow, wrap, binarization
import json
from data_utils import s3Dataset, localDataset
import os
import argparse
from tqdm import tqdm
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--chunk_num", type=int, default=1)
parser.add_argument("--chunk_idx", type=int, default=0)
parser.add_argument("--distortion", type=str, required=True)
# parser.add_argument("--data_name", type=str, required=True)
parser.add_argument("--target_folder", type=str, default="batch_distorted_images3")
# parser.add_argument("--target_folder", type=str, default="mnt/hwfile/opendatalab/chenjingzhou/cjz/opendatalab/cjz/MinerU/distortion_data/old")
parser.add_argument("--idx_folder", type=str, default="subset_idx")
parser.add_argument("--blur_psf_ratio", type=int, default=0.01)
args = parser.parse_args()

# data_dict = {
#     # 'mineru_cn1M':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn1M.json',
#     # },
#     # 'mineru_en1M':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en1M.json'
#     # },
#     # 'mineru_cn2M':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn2M.json',
#     # }, # 80k * 4+1
#     # 'mineru_en2M':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en2M.json'
#     # }, # 80k * 5
#     # 'table_cn440K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_zh440K.json'
#     # }, # 10k * 5
#     # 'table_en100K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_en100K.json'
#     # }, # 10k * 5
#     # 'exam_cn140K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#     #     'annotations':'/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_zh140K.json'
#     # }, # 10k * 5
#     'exam_en8K':{
#         'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#         'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_en8K.json'
#     }, # 1.6k * 5
#     # '3col_cn30K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_zh30K.json'
#     # }, # 2k * 5
#     # '3col_en20K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_en20K.json'
#     # }, # 2k * 5
#     # 'newspaper_cn60K':{
#     #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/newpaper_zh-700-K/v001/images/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_newspaper_zh60K.json'
#     # },
#     # 'numinamath_30w':{
#     #     'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot.json',
#     # }, 
#     # 'openmath_40w':{
#     #     'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2/',
#     #     'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2.json',
#     # }, # 10k * 5
#     } 

# data_dict = {
#     'test_set_20250113': {
#         'images': "/mnt/petrelfs/chenjingzhou/cjz/opendatalab/cjz/MinerU/doc_distortion_testset_1227/GT",
#         'annotations': "/mnt/petrelfs/chenjingzhou/cjz/opendatalab/cjz/MinerU/gt.json",
#         'no_subset_idx': True,
#     },
# }

data_dict = {
    # 'exam_cn140K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_exam_zh-140k.json",
    'mineru_cn2M': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_cn-2000k.json",
    'mineru_en2M': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_en-2000k.json",
    # 'table_cn440K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_table_zh-440k.json",
    # 'table_en100K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_table_en-100k.json",
    # 'exam_en8K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_exam_en-8k.json", # 用尽了
    # '3col_cn30K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_3col_zh-30k.json",
    # '3col_en20K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_3col_en-20k.json",
    # 'newspaper_cn60K': "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_newspaper_zh-60k.json",
    # 'math_cn200K': "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru_lvlm_data/mineru_math_cn200K.json",
    # 'math_en200K': "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru_lvlm_data/mineru_math_en200K.json",
}


distortion_2_postfix={
    'binarization': 1,
    'blur': 2,
    'shadow': 3,
    'wrap': 4,
    'none': 5,
}

if __name__ == '__main__':
    for data_name in data_dict.keys():
        print(f"***start to process {data_name}***", flush=True)
        idx_folder = args.idx_folder
        # data_name = args.data_name

        # postfix = "_third_sampling"
        # postfix = "_new"
        postfix = ""
        # image_folder =  data_dict[data_name]['images']
        # meta_data_path = data_dict[data_name]['annotations']
        meta_data_path = data_dict[data_name]
        
        with open(meta_data_path, 'r') as f:
            meta_data = json.load(f)
        print("1", flush=True)
        # if not data_dict[data_name].get("no_subset_idx", False):
        idxs1 = []
        for file in os.listdir(idx_folder):
            if file.startswith(data_name) and file.endswith(f"_{distortion_2_postfix[args.distortion]}{postfix}.txt"): # 第二次采样加了_new，第三次采样加了_third_sampling
                with open(os.path.join(idx_folder, file), "r") as f:
                    idxs1 = [int(idx.strip()) for idx in f.readlines()]
        
        if len(idxs1) == 0: # 测试集没有idx文件
            # raise ValueError(f"no idxs found for {data_name}")
            print(f"no idxs found for {data_name}", flush=True)
        else:
            meta_data = [meta_data[idx] for idx in idxs1]
        print("2", flush=True)

        # # ############ Save meta data ############
        meta_data_save_folder = "./meta_data_subset_first_second_sampling"
        os.makedirs(meta_data_save_folder, exist_ok=True)
        with open(os.path.join(meta_data_save_folder, f"{data_name}_{distortion_2_postfix[args.distortion]}{postfix}.json"), "w") as f: # 第二次采样加了_new，第三次采样加了_third_sampling
            json.dump(meta_data, f, indent=4, ensure_ascii=False)
        print(f"{data_name}_done")
        continue
        # # ########################################

        chunk_num = args.chunk_num
        chunk_idx = args.chunk_idx
        chunk_size = len(meta_data) // chunk_num
        if chunk_idx == chunk_num - 1:
            meta_data = meta_data[chunk_idx*chunk_size:]
        else:
            meta_data = meta_data[chunk_idx*chunk_size:(chunk_idx+1)*chunk_size]
        print(f"len(meta_data): {len(meta_data)}", flush=True)
        print("meta data done", flush=True)
        print("3", flush=True)

        # with open("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/subset_idx/mineru_en2M_200k_1.txt", "r") as f:
        #     idxs1 = [int(idx.strip()) for idx in f.readlines()]
        
        # print(len(meta_data))
        # print(max(idxs1))
        # meta_data_subset = [meta_data[idx] for idx in idxs1]

        # if image_folder.startswith("s3://"):
        if meta_data[0]["image"].startswith("mineru:s3://"):
            my_dataset = s3Dataset(meta_data=meta_data, folder="")
        else:
            my_dataset = localDataset(meta_data=meta_data, folder="")
        if args.distortion == "blur":
            my_distortion = blur(psf_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/psf", psf_size_mode = "interval", ratio = args.blur_psf_ratio)
        elif args.distortion == "shadow":
            # my_distortion = shadow(ink_color_range=(0, 0))
            my_distortion = shadow()
        elif args.distortion == "wrap":
            # my_distortion = wrap(ink_color_range=(0, 0))
            my_distortion = wrap()
        elif args.distortion == "binarization":
            my_distortion = binarization(ink_color_range=(0, 0))
        elif args.distortion == "none":
            my_distortion = lambda x: x
        else:
            raise ValueError(f"distortion {args.distortion} not supported")
        target_folder=args.target_folder
        # if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=True)

        # parallel_distort_images(my_dataset, my_distortion, target_folder, num_workers=4)

        for idx in tqdm(range(len(my_dataset))):
            try:
                image_name, image_data = my_dataset[idx]
                # 截取"mineru:s3://doc-parse-huawei/"以后的部分作为image_name，注意image_name第一个字符不能是/，否则会被认为是绝对路径
                image_name = image_name.split("mineru:s3://doc-parse-huawei/")[-1]
                path = os.path.join(target_folder, args.distortion, image_name)
                # print(f"target_folder: {target_folder}", flush=True)
                # print(f"image_name: {image_name}", flush=True)
                # print(f"path: {path}", flush=True)
                # exit()
                # 如果存在则跳过
                if os.path.exists(path):
                    continue
                distorted_image = my_distortion(image_data)
                # if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                cv2.imwrite(path, distorted_image)
            except Exception as e:
                print(path)
                print(f"error: {e}", flush=True)
                continue
        print(f"***finish processing {data_name}***", flush=True)