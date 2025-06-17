import json
import os

# 依次读取文件夹中所有json文件，打印第一条数据的id

folder="/mnt/hwfile/doc_parse/wufan/mineru2_data/train_data"

for filename in os.listdir(folder):
    if filename.endswith(".json"):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            print(filename)
            print(data[0])
            # if 'id' in data[0]:
            #     print(f"File: {filename}, ID: {data[0]['id']}")
            # else:
            #     print(f"File: {filename} does not contain 'id' key.")
