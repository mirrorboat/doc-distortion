from distortion_utils import parallel_distort_images, blur, shadow, wrap, binarization
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
parser.add_argument("--target_folder", type=str, default="batch_distorted_images2")
parser.add_argument("--idx_folder", type=str, default="subset_idx")
parser.add_argument("--blur_psf_ratio", type=int, default=0.01)
args = parser.parse_args()

data_dict = {
    # 'mineru_cn1M':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn1M.json',
    # },
    # 'mineru_en1M':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en1M.json'
    # },
    'mineru_cn2M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_cn2M.json',
    }, # 80k * 4+1
    'mineru_en2M':{
        'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
        'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en2M.json'
    }, # 80k * 5
    # 'table_cn440K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_zh440K.json'
    # }, # 10k * 5
    # 'table_en100K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_table_en100K.json'
    # }, # 10k * 5
    # 'exam_cn140K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
    #     'annotations':'/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_zh140K.json'
    # }, # 10k * 5
    # 'exam_en8K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_exam_en8K.json'
    # }, # 1.6k * 5
    # '3col_cn30K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/zh-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_zh30K.json'
    # }, # 2k * 5
    # '3col_en20K':{
    #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/en-10-M/v001/images/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_3col_en20K.json'
    # }, # 2k * 5
    # # 'newspaper_cn60K':{
    # #     'images': 's3://doc-parse-huawei/mineru2/inhouse-markdown/newpaper_zh-700-K/v001/images/',
    # #     'annotations': '/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_newspaper_zh60K.json'
    # # },
    # # 'numinamath_30w':{
    # #     'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot/',
    # #     'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/numinamath-cot.json',
    # # }, 
    # 'openmath_40w':{
    #     'images': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2/',
    #     'annotations': '/mnt/hwfile/opendatalab/zhaozhiyuan/mineru2.0_formula/dev/1218/openmathinstruct-2.json',
    # }, # 10k * 5
    } 

data_dict = {
    'test_set_20250113': {
        'images': "/mnt/petrelfs/chenjingzhou/cjz/opendatalab/cjz/MinerU/doc_distortion_testset_1227/GT",
        'annotations': "/mnt/petrelfs/chenjingzhou/cjz/opendatalab/cjz/MinerU/gt.json",
        'no_subset_idx': True,
    },
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
        print(f"***start to process {data_name}***")
        idx_folder = args.idx_folder
        # data_name = args.data_name

        image_folder =  data_dict[data_name]['images']
        meta_data_path = data_dict[data_name]['annotations']
        
        with open(meta_data_path, 'r') as f:
            meta_data = json.load(f)

        # if not data_dict[data_name].get("no_subset_idx", False):
        #     idxs1 = []
        #     for file in os.listdir(idx_folder):
        #         if file.startswith(data_name) and file.endswith(f"_{distortion_2_postfix[args.distortion]}_new.txt"): # 第二次采样加了_new
        #             with open(os.path.join(idx_folder, file), "r") as f:
        #                 idxs1 = [int(idx.strip()) for idx in f.readlines()]
            
        #     if len(idxs1) == 0:
        #         raise ValueError(f"no idxs found for {data_name}")

        #     meta_data = [meta_data[idx] for idx in idxs1]

        # ############ Save meta data ############
        # meta_data_save_folder = "./meta_data_subset"
        # if not os.path.exists(meta_data_save_folder):
        #     os.makedirs(meta_data_save_folder)
        # with open(os.path.join(meta_data_save_folder, f"{data_name}_{distortion_2_postfix[args.distortion]}_new.json"), "w") as f: # 第二次采样加了_new
        #     json.dump(meta_data, f, indent=4, ensure_ascii=False)
        # continue
        # ########################################

        chunk_num = args.chunk_num
        chunk_idx = args.chunk_idx
        chunk_size = len(meta_data) // chunk_num
        if chunk_idx == chunk_num - 1:
            meta_data = meta_data[chunk_idx*chunk_size:]
        else:
            meta_data = meta_data[chunk_idx*chunk_size:(chunk_idx+1)*chunk_size]
        print("meta data done")

        # with open("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/subset_idx/mineru_en2M_200k_1.txt", "r") as f:
        #     idxs1 = [int(idx.strip()) for idx in f.readlines()]
        
        # print(len(meta_data))
        # print(max(idxs1))
        # meta_data_subset = [meta_data[idx] for idx in idxs1]

        if image_folder.startswith("s3://"):
            my_dataset = s3Dataset(meta_data=meta_data, folder=image_folder)
        else:
            my_dataset = localDataset(meta_data=meta_data, folder=image_folder)
        if args.distortion == "blur":
            my_distortion = blur(psf_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/psf", args.blur_psf_ratio)
        elif args.distortion == "shadow":
            my_distortion = shadow(ink_color_range=(0, 0))
        elif args.distortion == "wrap":
            my_distortion = wrap(ink_color_range=(0, 0))
        elif args.distortion == "binarization":
            my_distortion = binarization(ink_color_range=(0, 0))
        elif args.distortion == "none":
            my_distortion = lambda x: x
        else:
            raise ValueError(f"distortion {args.distortion} not supported")
        target_folder=args.target_folder
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # parallel_distort_images(my_dataset, my_distortion, target_folder, num_workers=4)

        for idx in tqdm(range(len(my_dataset))):
            try:
                image_name, image_data = my_dataset[idx]
                path=os.path.join(target_folder, args.distortion, image_name)
                # 如果存在则跳过
                if os.path.exists(path):
                    continue
                distorted_image = my_distortion(image_data)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                cv2.imwrite(path, distorted_image)
            except Exception as e:
                print(f"error: {e}", flush=True)
                continue