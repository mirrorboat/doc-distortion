import boto3
import random

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}

def get_s3_client(config):
    session = boto3.Session(
        aws_access_key_id=config['ak'],
        aws_secret_access_key=config['sk']
    )
    return session.client('s3', endpoint_url=config['endpoint'])

s3_client = get_s3_client(s3_load_cfg_huawei)

def list_s3_folder_structure(client, bucket: str, prefix: str):
    # Ensure the prefix ends with a slash
    if not prefix.endswith("/"):
        prefix += "/"
    
    folder_counts = {}
    
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')
    
    for page in pages:
        # Process common prefixes (subfolders)
        if 'CommonPrefixes' in page:
            for common_prefix in page['CommonPrefixes']:
                subfolder = common_prefix['Prefix']
                folder_counts[subfolder] = 0
        
        # Process objects (files)
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                folder = os.path.dirname(key) + "/"
                
                if folder not in folder_counts:
                    folder_counts[folder] = 0
                
                folder_counts[folder] += 1
    
    # Sort folders by depth and then alphabetically
    sorted_folders = sorted(folder_counts.keys(), key=lambda x: (x.count('/'), x))
    
    print("Folder Structure and File Counts:")
    for folder in sorted_folders:
        count = folder_counts[folder]
        print(f"{folder}: {count} files")

# Example usage
if __name__ == "__main__":
    s3_bucket_name = "doc-parse-huawei"         # Your S3 bucket name
    s3_prefix = "test_jingzhou/distortion"       # The prefix (folder structure) in S3

    list_s3_folder_structure(s3_client, s3_bucket_name, s3_prefix)
