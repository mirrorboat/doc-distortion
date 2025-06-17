from petrel_client.client import Client
import json
from tqdm import tqdm
data_path = "/mnt/hwfile/doc_parse/lz/Final1/Formula-400k/mineru2_formula-distortion_100k.json"
with open(data_path, 'r') as f:
    data = json.load(f)

client = Client()

for item in tqdm(data):
    try:
        image_bytes = client.get(item["image"])
    except:
        print(item["image"])
