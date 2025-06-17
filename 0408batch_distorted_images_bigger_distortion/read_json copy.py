import json
import os


with open("/mnt/hwfile/opendatalab/bigdata_mineru/zhaozhiyuan/refine_md_formula/table_500k_html.json", 'r') as f:
    data = json.load(f)
    print(data[0])
