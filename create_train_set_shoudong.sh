#!/bin/bash

# 手动指定需要执行的任务和对应的chunk ID组合

declare -a task_chunk_list=(
    "none 13"
    "none 21"
    "none 27"
    "none 28"
    "none 31"
)

for task_chunk in "${task_chunk_list[@]}"
do
    # 解析task和chunk_idx
    task=$(echo $task_chunk | awk '{print $1}')
    CHUNK_IDX=$(echo $task_chunk | awk '{print $2}')

    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./log/${task}_chunk_${CHUNK_IDX}_output.txt
#SBATCH --error=./log/${task}_chunk_${CHUNK_IDX}_error.txt
#SBATCH --job-name=${CHUNK_IDX}t${task}

python batch_distortion.py \
    --chunk_num 32 \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done