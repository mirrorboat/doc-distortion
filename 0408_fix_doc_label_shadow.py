import json
import os
from tqdm import tqdm
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("--chunk_num", type=int, default=1000)
# parser.add_argument("--chunk_idx", type=int, default=0)
# parser.add_argument("--distortion", type=str, required=True)
# args = parser.parse_args()

distortion='shadow'

def load_json_file(file_path):
    """
    加载 JSON 文件并返回其内容。
    
    :param file_path: JSON 文件路径
    :return: JSON 数据（字典或列表）
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, file_path):
    """
    将数据保存为 JSON 文件。
    
    :param data: 要保存的数据（字典或列表）
    :param file_path: 输出文件路径
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def replace_conversations(source_data, corrected_datasets):
    """
    根据 id 匹配源数据集和修正数据集，替换源数据集的 conversations。
    
    :param source_data: 源数据集，列表形式，每个元素是一个 JSON 对象
    :param corrected_datasets: 多个修正数据集，列表形式，每个元素是一个 JSON 对象列表
    :return: 替换后的源数据集
    """
    # 创建一个字典，用于快速查找修正数据集中对应的 conversations
    corrected_dict = {}
    for dataset in corrected_datasets:
        for item in dataset:
            correct_prefix="mineru:s3://doc-parse-huawei"
            item_id = item["image"].removeprefix(correct_prefix)
            corrected_dict[item_id] = item['conversations']
    # 遍历源数据集，进行替换
    failed_idxs = []
    for idx, source_item in tqdm(enumerate(source_data)):
        # source_id = source_item['id']
        source_prefix=f"s3://doc-parse-huawei/test_jingzhou/distortion/batch_distorted_images_bigger_distortion/{distortion}"
        source_id = source_item["image"].removeprefix(source_prefix)
        # if source_id in corrected_dict:
        #     # 使用修正数据集中的 conversations 替换源数据集中的 conversations
        #     source_item['conversations'] = corrected_dict[source_id]
        # else:
        #     print(f"Warning: ID {source_id} not found in any corrected dataset.")
        try:
            source_item['conversations'] = corrected_dict[source_id]
        except KeyError:
            failed_idxs.append(idx)
            print(f"Warning: ID {source_id} not found in any corrected dataset.")

    print(f"Warning: {len(failed_idxs)} IDs not found in any corrected dataset.")
    # 根据failed_idxs指定的序号，从源数据集中删除没有对应修正数据集的项
    success_idxs = [i for i in range(len(source_data)) if i not in failed_idxs]
    source_data_subset = [source_data[i] for i in success_idxs]
    print(f"len(source_data): {len(source_data_subset)}")

    return source_data_subset



# 主函数
def main(source_file_path, corrected_file_paths, output_file_path):
    """
    主函数：读取源数据集和修正数据集，替换 conversations 并保存结果。
    
    :param source_file_path: 源数据集的 JSON 文件路径
    :param corrected_file_paths: 修正数据集的 JSON 文件路径列表
    :param output_file_path: 输出文件路径
    """
    # 加载源数据集
    source_data = load_json_file(source_file_path)
    
    # 加载所有修正数据集
    corrected_datasets = []
    for file_path in corrected_file_paths:
        corrected_data = load_json_file(file_path)
        corrected_datasets.append(corrected_data)
    
    # 替换 conversations
    updated_source_data = replace_conversations(source_data, corrected_datasets)
    
    # 保存更新后的源数据集
    save_json_file(updated_source_data, output_file_path)
    print(f"Updated source data saved to {output_file_path}")


# 示例用法
if __name__ == "__main__":
    # 源数据集文件路径
    source_file_path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_third_sampling/all_3_bigger_distortion_new_path_211931.json"
    
    # 修正数据集文件路径列表
    corrected_file_paths = [
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_cn-1000k_merged_qwen.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_en-1000k_merged_qwen.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_exam_en-8k_merged.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/mineru_math_cn200K_merged.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_cn-2000k_merged_qwen.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_en-2000k_merged_qwen.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/Mineru_exam_zh-140k_merged.json",
        "/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data/mineru_math_en200K_merged.json",
        "/mnt/hwfile/opendatalab/bigdata_mineru/zhaozhiyuan/refine_md_formula/table_500k_html.json",
    ]
    
    # 输出文件路径
    output_file_path = f"/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/fix_label/{distortion}.json"
    
    # 执行主函数
    main(source_file_path, corrected_file_paths, output_file_path)