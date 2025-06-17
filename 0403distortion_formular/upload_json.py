from petrel_client.client import Client

conf_path = '~/petreloss.conf'
client = Client(conf_path)
with open("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/0403distortion_formular/formular_distortion_fix_label_100k.json", 'rb') as file_data:
    bytes = file_data.read()
    client.put('cluster_huawei:' + "s3://doc-parse-huawei/mineru2/distortion/0430/formular_distortion_fix_label_100k.json", bytes)