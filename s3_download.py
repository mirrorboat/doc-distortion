import os
from s3_utils import get_s3_client, list_s3_objects_detailed
import random
from tqdm import tqdm

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def download_s3_folder_to_local(s3_bucket: str, s3_prefix: str, local_folder_path: str):
    # Ensure the prefix ends with a slash
    if not s3_prefix.endswith("/"):
        s3_prefix += "/"
    
    # Ensure the local folder path exists
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    
    # List all objects under the source prefix
    objects_to_download = []
    for content in list_s3_objects_detailed(s3_client, f"s3://{s3_bucket}/{s3_prefix}", recursive=True):
        key = content[0].split(f"s3://{s3_bucket}/")[1]
        if key.endswith(".txt"):
            objects_to_download.append(key)
    
    objects_to_download=objects_to_download[31:]
    print("**********warning***")

    total_objects = len(objects_to_download)
    
    print(f"Found {total_objects} objects to download.")
    # Download each object to the local folder
    for i, key in tqdm(enumerate(objects_to_download, start=1)):
        local_file_path = os.path.join(local_folder_path, key.lstrip(s3_prefix))
        
        # Create necessary directories
        local_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        
        try:
            s3_client.download_file(s3_bucket, key, local_file_path)
            print(f"[{i}/{total_objects}] Downloaded {key} to {local_file_path}", flush=True)
        except Exception as e:
            print(f"[{i}/{total_objects}] Error downloading {key}: {e}", flush=True)

# Example usage
if __name__ == "__main__":
    # s3_bucket_name = "doc-parse-huawei"         # Source S3 bucket name
    # s3_prefix = "test_jingzhou/distortion/batch_distorted_images3/none"       # Source prefix (folder structure) in S3
    # local_folder_path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images3"   # Local folder path to save the files


    s3_bucket_name = "doc-parse-huawei"         # Source S3 bucket name
    s3_prefix = "mineru2/synthdog/language/WanJuan/WebText-en/"       # Source prefix (folder structure) in S3
    local_folder_path = "/mnt/petrelfs/chenjingzhou/cjz/data/wangjuan/en"   # Local folder path to save the files

    download_s3_folder_to_local(s3_bucket_name, s3_prefix, local_folder_path)
    print(f"All contents in s3://{s3_bucket_name}/{s3_prefix} have been downloaded to {local_folder_path}.")

