import os
import glob
import linecache

# 指定你要检查的目录路径
specified_dir = '/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/log_s2write2'  
# specified_dir = '/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/log'  

# 查找所有以output.txt结尾的文件
files = glob.glob(os.path.join(specified_dir, '*output.txt'))

ls = []
print(len(files))
for file_path in files:
    try:
        # 读取文件的最后一行
        with open(file_path, 'r') as file:
            # 移动到文件的最后一行
            last_line = file.readlines()[-1].strip()

        # 检查最后一行是否为'***finish processing math_en200K***'
        if 'done' not in last_line:
            # print(f"File: {file_path} does not end with the expected line.")
            ls.append(file_path)
    except Exception as e:
        print(f"Could not process file {file_path}: {e}")

print("i")
# 排序
ls.sort()
for filename in ls:
    print(filename)