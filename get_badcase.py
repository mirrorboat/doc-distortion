from s3_utils import get_s3_client, list_s3_objects, read_s3_object_content
import random
import os


ip_idx = random.choice(range(164-129)) + 129

# for savety, we delete quyuan's ak and sk from ouyanglinke
s3_load_cfg = {'endpoint': f'http://p-ceph-norm-outside.pjlab.org.cn', 'ak': '', 'sk': ''}
s3_client = get_s3_client("", s3_load_cfg)

source="s3://llm-qatest-pnorm/quyuan/Minerubadcase/online-demo"
target="./Minerubadcase-online-demo"
datas=list_s3_objects(s3_client, source)
print("datas done")
# for data in datas:
#     print(data)

# 将source文件夹下载到本地
if not os.path.exists(target):
    os.makedirs(target)

for data in datas:
    content=read_s3_object_content(s3_client, data)
    data_name=data.split("/")[-1]
    with open(os.path.join(target, data_name), "wb") as f:
        f.write(content)

