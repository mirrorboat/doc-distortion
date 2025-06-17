import json

path="/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/tmp/train-677e0db8a461-000100.bin"

# 将前10条数据保存到subset10.jsonl
with open(path, 'r') as f:
    for i in range(10):
        line = f.readline()
        with open('/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/tmp/subset10.jsonl', 'a') as f2:
            f2.write(line)