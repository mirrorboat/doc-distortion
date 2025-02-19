#!/bin/bash

TASK_NUM=8

for TASK_IDX in $(seq 0 $((TASK_NUM - 1)))
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./add_prefix_log/${TASK_IDX}_output.txt   # 标准输出文件
#SBATCH --error=./add_prefix_log/${TASK_IDX}_error.txt     # 错误输出文件

python add_image_path_prefix.py
EOT
done