# from s3_utils import get_s3_client, write_s3_object_content
# import os
# from tqdm import tqdm
# import random

# # 10.140.96.129 ~ 10.140.96.164
# ip_idx = random.choice(range(164-129)) + 129

# s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
# s3_client = get_s3_client("", s3_load_cfg_huawei)

# def upload_folder_to_s3(local_folder_path: str, s3_bucket: str, s3_prefix: str):
#     # Ensure the prefix ends with a slash
#     if not s3_prefix.endswith("/"):
#         s3_prefix += "/"
    
#     # Collect all files to upload
#     files_to_upload = []
#     for root, dirs, files in os.walk(local_folder_path):
#         for file in files:
#             local_file_path = os.path.join(root, file)
#             relative_path = os.path.relpath(local_file_path, local_folder_path)
#             s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
#             files_to_upload.append((local_file_path, s3_key))
    
#     total_files = len(files_to_upload)
    
#     with tqdm(total=total_files, desc="Uploading files", unit="file") as pbar:
#         for local_file_path, s3_key in files_to_upload:
#             with open(local_file_path, "rb") as f:
#                 file_data = f.read()
            
#             write_s3_object_content(s3_client, f"s3://{s3_bucket}/{s3_key}", file_data)
#             pbar.update(1)
#             # print(f"Uploaded {local_file_path} to s3://{s3_bucket}/{s3_key}")

# # Example usage
# if __name__ == "__main__":
#     local_folder_path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250113_testset"  # Replace with your local folder path
#     s3_bucket_name = "doc-parse-huawei"         # Your S3 bucket name
#     s3_prefix = "test_jingzhou/distortion"      # The prefix (folder structure) in S3

#     upload_folder_to_s3(local_folder_path, s3_bucket_name, s3_prefix)





from s3_utils import get_s3_client, write_s3_object_content
import os
from tqdm import tqdm
import random

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def upload_folder_to_s3(local_folder_path: str, s3_bucket: str, s3_prefix: str):
    # Ensure the prefix ends with a slash
    if not s3_prefix.endswith("/"):
        s3_prefix += "/"
    
    # Get the source folder name from the local path
    source_folder_name = os.path.basename(os.path.normpath(local_folder_path))
    s3_full_prefix = os.path.join(s3_prefix, source_folder_name).replace("\\", "/")
    
    # Collect all files to upload
    files_to_upload = []
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            s3_key = os.path.join(s3_full_prefix, relative_path).replace("\\", "/")
            files_to_upload.append((local_file_path, s3_key))
    
    total_files = len(files_to_upload)
    
    count = 0
    with tqdm(total=total_files, desc="Uploading files", unit="file") as pbar:
        for local_file_path, s3_key in files_to_upload:
            with open(local_file_path, "rb") as f:
                file_data = f.read()
            
            write_s3_object_content(s3_client, f"s3://{s3_bucket}/{s3_key}", file_data)
            pbar.update(1)
            count += 1
            if count % 8192 == 0:
                print(f"{count}/{total_files}", flush=True)
            # print(f"Uploaded {local_file_path} to s3://{s3_bucket}/{s3_key}")

# Example usage
if __name__ == "__main__":
    local_folder_path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images3"  # Replace with your local folder path
    s3_bucket_name = "doc-parse-huawei"         # Your S3 bucket name
    s3_prefix = "test_jingzhou/distortion"      # The prefix (folder structure) in S3

    upload_folder_to_s3(local_folder_path, s3_bucket_name, s3_prefix)


