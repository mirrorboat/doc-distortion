import os
import json
from s3_utils import get_s3_client, write_s3_object_content
import boto3
import random
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Upload images to S3 from a JSON file.')
parser.add_argument('--json_file_path', type=str, help='The path to the JSON file containing the image paths.')
parser.add_argument('--chunk_num', type=int, help='The chunk number of the json file.')
parser.add_argument('--chunk_id', type=int, help='The chunk number of the json file.')
args = parser.parse_args()

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def upload_images_from_json(json_file_path: str, base_local_path: str, s3_bucket: str, s3_prefix: str):
    # Ensure the base local path ends with a slash
    if not base_local_path.endswith("/"):
        base_local_path += "/"
    
    # Ensure the S3 prefix ends with a slash
    if not s3_prefix.endswith("/"):
        s3_prefix += "/"
    
    # Read and parse the JSON file
    with open(json_file_path, "r") as f:
        data = json.load(f)

    if args.chunk_id == args.chunk_num - 1:
        data = data[args.chunk_id * len(data) // args.chunk_num:]
    else:
        data = data[args.chunk_id * len(data) // args.chunk_num:(args.chunk_id + 1) * len(data) // args.chunk_num]
    
    total_images = len(data)
    print(f"Found {total_images} images to upload.")
    
    for i, item in tqdm(enumerate(data, start=1)):
        image_path = item.get("image")
        if not image_path:
            print(f"[{i}/{total_images}] Skipping item without image_path: {item}")
            continue
        
        # Ensure the image path starts with the base local path
        if not image_path.startswith(base_local_path):
            print(f"[{i}/{total_images}] Skipping invalid image_path: {image_path}")
            continue
        
        # Calculate the relative path
        relative_path = os.path.relpath(image_path, base_local_path)
        
        # Construct the S3 key
        s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
        
        try:
            # Open and read the image file
            with open(image_path, "rb") as f:
                file_data = f.read()
            
            # Upload the file to S3
            write_s3_object_content(s3_client, f"s3://{s3_bucket}/{s3_key}", file_data)
            # print(f"[{i}/{total_images}] Uploaded {image_path} to s3://{s3_bucket}/{s3_key}")
        except Exception as e:
            print(f"[{i}/{total_images}] Error uploading {image_path}: {e}")

# Example usage
if __name__ == "__main__":
    json_file_path = args.json_file_path
    base_local_path = "/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/batch_distorted_images_bigger_distortion"
    s3_bucket_name = "doc-parse-huawei"         # Your S3 bucket name
    s3_prefix = "test_jingzhou/distortion/batch_distorted_images_bigger_distortion"  # The prefix (folder structure) in S3

    upload_images_from_json(json_file_path, base_local_path, s3_bucket_name, s3_prefix)
    print(f"All images from {json_file_path} have been uploaded to s3://{s3_bucket_name}/{s3_prefix}.")



