from s3_utils import get_s3_client, list_s3_objects
import random

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def list_s3_folders(client, path: str):
    # Ensure the path ends with a slash
    if not path.endswith("/"):
        path += "/"
    
    folders = []
    for content in list_s3_objects(client, path, recursive=False, is_prefix=True):
        # Remove the leading and trailing slashes to get the folder name
        folder_name = content.rstrip("/").split("/")[-1]
        folders.append(folder_name)
    
    return folders

def list_s3_files(client, path: str):
    # Ensure the path ends with a slash
    if not path.endswith("/"):
        path += "/"
    
    files = []
    for content in list_s3_objects(client, path, recursive=True):
        # Remove the leading bucket name to get the file path
        file_path = content[len(path):]
        files.append(file_path)
    
    return files

# Example usage
if __name__ == "__main__":
    # s3_path = "s3://doc-parse-huawei/mineru2/inhouse-markdown"
    # s3_path = "s3://doc-parse-huawei"
    # s3_path = "s3://doc-parse-huawei/test_jingzhou/distortion/batch_distorted_images3"
    # s3_path = "s3://doc-parse-huawei/mineru2/synthdog/coco_img/train2017/"
    # s3_path = "s3://doc-parse-huawei"
    # s3_path = "s3://llm-process-pperf/wanjuan-cc-en-new/v001/200b/"
    # s3_path = "s3://llm-process-pperf/wanjuan-cc-en-new/v001/100b/"
    s3_path = "s3://doc-parse-huawei/mineru2/synthdog/language/WanJuan/"
    # s3_path = "s3://doc-parse-huawei/test_jingzhou/distortion/batch_distorted_images3/blur/mineru2/inhouse-markdown/en-10-M"
    folders = list_s3_folders(s3_client, s3_path)
    print("Folders in", s3_path, ":")
    for folder in folders:
        print(folder)

    # files = list_s3_files(s3_client, s3_path)
    # print("Files in", s3_path, ":")
    # print(len(files))
    # for file in files:
    #     print(file)