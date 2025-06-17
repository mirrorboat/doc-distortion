import json

path = "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_en-2000k.json"

with open(path, 'r') as f:
    meta_data = json.load(f)

print(meta_data[0])
print(meta_data[-1])
print(len(meta_data))