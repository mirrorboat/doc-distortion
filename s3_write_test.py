# from s3_utils import get_s3_client, write_s3_object_content
# import cv2
# import numpy as np
# import os

# # 10.140.96.129 ~ 10.140.96.164
# ip_idx = random.choice(range(164-129)) + 129

# s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
# s3_client = get_s3_client("", s3_load_cfg_huawei)

# def upload_image_to_s3(image_path: str, s3_bucket: str, s3_key: str):
#     # Read the image using OpenCV
#     image = cv2.imread(image_path)
    
#     if image is None:
#         raise ValueError(f"Image not found or unable to read at path: {image_path}")

#     # Encode the image into JPEG format in memory
#     _, buffer = cv2.imencode('.jpg', image)
#     image_data = np.array(buffer).tobytes()

#     # Upload the image data to S3
#     write_s3_object_content(s3_client, f"s3://{s3_bucket}/{s3_key}", image_data)
#     print(f"Image uploaded successfully to s3://{s3_bucket}/{s3_key}")

# # Example usage
# if __name__ == "__main__":
#     local_image_path = "path/to/local/image.jpg"  # Replace with your local image path
#     s3_bucket_name = "your-bucket-name"          # Replace with your S3 bucket name
#     s3_object_key = "images/uploaded-image.jpg"   # Replace with your desired object key in S3

#     upload_image_to_s3(local_image_path, s3_bucket_name, s3_object_key)



from s3_utils import get_s3_client, write_s3_object_content, put_s3_object
import cv2
import numpy as np
import os
import random

# 10.140.96.129 ~ 10.140.96.164
ip_idx = random.choice(range(164-129)) + 129

s3_load_cfg_huawei = {'endpoint': f'http://10.140.96.{ip_idx}', 'ak': 'C572089C522D2646C39F', 'sk': 'EKZQwqlKwU3MaooDoIpw68Kv1xEAAAGTUi0mRvxh'}
s3_client = get_s3_client("", s3_load_cfg_huawei)

def create_folder_in_s3(client, bucket: str, folder_name: str):
    # Ensure the folder name ends with a slash
    if not folder_name.endswith("/"):
        folder_name += "/"
    
    # Create an empty object to simulate a folder
    client.put_object(Bucket=bucket, Key=folder_name, Body='')

def upload_image_to_s3(image_path: str, s3_bucket: str, s3_key: str):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Image not found or unable to read at path: {image_path}")

    # Encode the image into JPEG format in memory
    _, buffer = cv2.imencode('.jpg', image)
    image_data = np.array(buffer).tobytes()

    # Upload the image data to S3
    write_s3_object_content(s3_client, f"s3://{s3_bucket}/{s3_key}", image_data)
    print(f"Image uploaded successfully to s3://{s3_bucket}/{s3_key}")

# Example usage
if __name__ == "__main__":
    local_image_path = "/mnt/petrelfs/chenjingzhou/cjz/test.png"  # Replace with your local image path
    s3_bucket_name = "doc-parse-huawei"          # Your S3 bucket name
    folder_name = "test_jingzhou/distortion"             # The folder you want to create
    image_filename = "test.png"          # The filename for the uploaded image

    create_folder_in_s3(s3_client, s3_bucket_name, folder_name)

    s3_key = os.path.join(folder_name, image_filename)

    upload_image_to_s3(local_image_path, s3_bucket_name, s3_key)

