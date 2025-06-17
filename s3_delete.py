from s3_utils import get_s3_client, list_s3_objects_detailed
import boto3
import random
from tqdm import tqdm

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def delete_s3_folder_contents(client, bucket: str, prefix: str):
    # Ensure the prefix ends with a slash
    if not prefix.endswith("/"):
        prefix += "/"
    
    # List all objects and common prefixes (folders) under the given prefix
    objects_to_delete = []
    for content in tqdm(list_s3_objects_detailed(client, f"s3://{bucket}/{prefix}")):
        key = content[0].split(f"s3://{bucket}/")[1]
        objects_to_delete.append({'Key': key})
        
        # Delete objects in batches of 1000
        if len(objects_to_delete) >= 1000:
            client.delete_objects(Bucket=bucket, Delete={'Objects': objects_to_delete}, ChecksumAlgorithm="SHA256")
            objects_to_delete = []
    
    # Delete any remaining objects
    if objects_to_delete:
        client.delete_objects(Bucket=bucket, Delete={'Objects': objects_to_delete})

# Example usage
if __name__ == "__main__":
    s3_bucket_name = "doc-parse-huawei"         # Your S3 bucket name
    s3_prefix = "test_jingzhou/distortion/batch_distorted_images3"      # The prefix (folder structure) in S3

    delete_s3_folder_contents(s3_client, s3_bucket_name, s3_prefix)
    print(f"All contents in s3://{s3_bucket_name}/{s3_prefix} have been deleted.")
