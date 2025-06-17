import json

path = "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru2_data/mineru_en2M.json"

with open(path, 'r') as f:
    meta_data = json.load(f)

print(meta_data[0])
print(meta_data[-1])
print(len(meta_data))