#!/bin/bash

# 设置chunk_num为8，因为总共有8个chunk需要处理
CHUNK_NUM=8

# 循环从0到CHUNK_NUM-1
for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
    # 使用sbatch提交每个任务到Slurm队列，并且将输出重定向到特定的文件
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./log/binarization_chunk_${CHUNK_IDX}_output.txt   # 标准输出文件
#SBATCH --error=./log/binarization_chunk_${CHUNK_IDX}_error.txt     # 错误输出文件

python batch_distortion.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion binarization
EOT
done