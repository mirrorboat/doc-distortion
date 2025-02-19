#!/bin/bash

CHUNK_NUM=16

for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./log/none_chunk_${CHUNK_IDX}_output_new.txt   # 标准输出文件
#SBATCH --error=./log/none_chunk_${CHUNK_IDX}_error_new.txt     # 错误输出文件

python batch_distortion.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion none
EOT
done