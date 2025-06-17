import json

# path = "/mnt/hwfile/opendatalab/zhangrui/shared_data/mineru_lvlm_data/mineru_math_en200K.json"
path = "/mnt/hwfile/opendatalab/liuzheng/Mineru/dataset/Stage2/Mineru_exam_zh-140k.json"
with open(path, 'r') as f:
    meta_data = json.load(f)

print(meta_data[0])
print(meta_data[-1])
print(len(meta_data))