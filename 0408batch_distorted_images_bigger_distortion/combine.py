import json
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("--chunk_num", type=int, default=1000)
# parser.add_argument("--chunk_idx", type=int, default=0)
# parser.add_argument("--distortion", type=str, required=True)
# parser.add_argument("--target_folder", type=str, default="0403distortion_note")
# args = parser.parse_args()

chunk_num=32
task="warp"
all_data=[]
for chunk in range(chunk_num):
    path = f"mineru2_doc_{task}_{chunk:02d}_{chunk_num:02d}.json"
    with open(path, 'r') as f:
        data = json.load(f)
        all_data.extend(data)

# save
path = f"mineru2_doc_{task}_combine_{len(all_data)}.json"
with open(path, 'w') as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)