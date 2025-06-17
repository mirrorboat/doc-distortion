from distortion_utils_small_image import blur, shadow, wrap, binarization
import json
from data_utils import s3Dataset, localDataset
import os
import argparse
from tqdm import tqdm
import cv2
import re
from petrel_client.client import Client

parser = argparse.ArgumentParser()
parser.add_argument("--chunk_num", type=int, default=100)
parser.add_argument("--chunk_idx", type=int, default=0)
parser.add_argument("--distortion", type=str, required=True)
parser.add_argument("--target_folder", type=str, default="0403distortion_table")
args = parser.parse_args()


folder="/mnt/hwfile/opendatalab/bigdata_mineru/liuzheng/Mineru/dataset/Final/Table-350k"
file_dict={
    "mineru2_financial-report-table_pure-table_2k.json": 1,
    "mineru2_mmtab_pure-table_10k.json": 1, # 每隔2取1个
    "mineru2_table-eval-data_pure-table_6k.json": 1,
    "mineru2_pubtabnet_pure-table_90k.json": 1,
    "mineru2_sparse_pure-table_150k.json": 2,
}
file_dict = {os.path.join(folder, file_name): interval for file_name, interval in file_dict.items()}

distortion_2_postfix={
    'binarization': 1,
    'blur': 2,
    'shadow': 3,
    'warp': 4,
}


# def extract_and_join(text):
#     # 定义正则表达式，匹配<|md_start|>和<|md_end|>之间的内容
#     pattern = r'<\|md_start\|>(.*?)<\|md_end\|>'
#     matches = re.findall(pattern, text, re.DOTALL)
#     result = '\n\n'.join(matches)
    
#     return result


if __name__ == '__main__':
    s3_prefix="s3://doc-parse-huawei/mineru2/distortion/"
    for meta_data_path in file_dict.keys():
        print(f"***start to process {meta_data_path}***", flush=True)

        with open(meta_data_path, 'r') as f:
            meta_data = json.load(f)

        chunk_num = args.chunk_num
        chunk_idx = args.chunk_idx
        chunk_size = len(meta_data) // chunk_num
        if chunk_idx == chunk_num - 1:
            meta_data = meta_data[chunk_idx*chunk_size:]
        else:
            meta_data = meta_data[chunk_idx*chunk_size:(chunk_idx+1)*chunk_size]
        # 依据file_dict确认的间隔，按照固定间隔取出子集
        meta_data = meta_data[::file_dict[meta_data_path]]
        meta_data = meta_data[distortion_2_postfix[args.distortion]::len(distortion_2_postfix)]
        
        print(f"len(meta_data): {len(meta_data)}", flush=True)

        # if image_folder.startswith("s3://"):
        if meta_data[0]["image"].startswith("mineru:s3://") or meta_data[0]["image"].startswith("s3://"):
            my_dataset = s3Dataset(meta_data=meta_data, folder="")
        else:
            # raise ValueError(f"Please check if the image is really in local")
            my_dataset = localDataset(meta_data=meta_data, folder="")
        if args.distortion == "blur":
            my_distortion = blur(psf_folder="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/psf_subset", psf_size_mode = "ratio")
        elif args.distortion == "shadow":
            # my_distortion = shadow(ink_color_range=(0, 0))
            my_distortion = shadow()
        elif args.distortion == "warp":
            # my_distortion = wrap(ink_color_range=(0, 0))
            my_distortion = wrap()
        elif args.distortion == "binarization":
            # my_distortion = binarization(ink_color_range=(0, 0))
            my_distortion = binarization()
        elif args.distortion == "none":
            my_distortion = lambda x: x
        else:
            raise ValueError(f"distortion {args.distortion} not supported")
        target_folder=args.target_folder
        # if not os.path.exists(target_folder):
        # os.makedirs(target_folder, exist_ok=True)


        for idx in tqdm(range(len(my_dataset))):
            try:
                image_name, image_data = my_dataset[idx]
                # 截取"mineru:s3://doc-parse-huawei/"以后的部分作为image_name，注意image_name第一个字符不能是/，否则会被认为是绝对路径
                # image_name = image_name.split("mineru:s3://doc-parse-huawei/")[-1]
                image_name = image_name.split("/mnt/hwfile/opendatalab/bigdata_mineru/wufan/data/")[-1]
                local_image_filepath = os.path.join(target_folder, args.distortion, image_name)
                s3_image_path = os.path.join(s3_prefix, args.distortion, image_name)

                distorted_image = my_distortion(image_data)
                if not os.path.exists(os.path.dirname(local_image_filepath)):
                    os.makedirs(os.path.dirname(local_image_filepath))
                cv2.imwrite(local_image_filepath, distorted_image)
                client = Client()
                with open(local_image_filepath, 'rb') as file_data:
                    img_bytes = file_data.read()
                    client.put('cluster_huawei:' + s3_image_path, img_bytes)
                os.remove(local_image_filepath)
            except Exception as e:
                print(local_image_filepath)
                print(f"error: {e}", flush=True)
                continue
        print(f"***finish processing {meta_data_path}***", flush=True)

    all_meta_data=[]
    for meta_data_path in file_dict.keys():
        print(f"***start to save {meta_data_path}***", flush=True)
        
        with open(meta_data_path, 'r') as f:
            meta_data = json.load(f)

        chunk_num = args.chunk_num
        chunk_idx = args.chunk_idx
        chunk_size = len(meta_data) // chunk_num
        if chunk_idx == chunk_num - 1:
            meta_data = meta_data[chunk_idx*chunk_size:]
        else:
            meta_data = meta_data[chunk_idx*chunk_size:(chunk_idx+1)*chunk_size]
        # 依据file_dict确认的间隔，按照固定间隔取出子集
        meta_data = meta_data[::file_dict[meta_data_path]]
        meta_data = meta_data[distortion_2_postfix[args.distortion]::len(distortion_2_postfix)]
        
        print(f"len(meta_data): {len(meta_data)}", flush=True)
        all_meta_data += meta_data

    for data in all_meta_data:
        image_name = data["image"].split("/mnt/hwfile/opendatalab/bigdata_mineru/wufan/data/")[-1]
        data["image"] = os.path.join(s3_prefix, args.distortion, image_name)
        data["distortion_type"] = args.distortion
        # data["conversations"][1]["value"] = extract_and_join(data["conversations"][1]["value"])

    target_meta_data_path = os.path.join(target_folder, f"mineru2_table_{args.distortion}_{args.chunk_idx:02d}_{args.chunk_num:02d}.json")
    with open(target_meta_data_path, "w", encoding='utf-8') as f:
        json.dump(all_meta_data, f, indent=4, ensure_ascii=False)

