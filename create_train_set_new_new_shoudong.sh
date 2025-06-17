#!/bin/bash

# 手动指定需要执行的任务和对应的chunk ID组合
declare -a task_chunk_list=(
    "binarization 8"
    "binarization 9"
    "binarization 10"
    "binarization 29"
    "binarization 30"
    "binarization 31"
    "shadow 1"
    "shadow 3"
    "wrap 10"
    "wrap 11"
    "wrap 12"
    "wrap 16"
    "wrap 17"
    "wrap 21"
    "wrap 24"
    "wrap 31"
)

for task_chunk in "${task_chunk_list[@]}"
do
    # 解析task和chunk_idx
    task=$(echo $task_chunk | awk '{print $1}')
    CHUNK_IDX=$(echo $task_chunk | awk '{print $2}')

    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=s2_bigdata
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./log_more_distortion_new/${task}_chunk_${CHUNK_IDX}_output.txt
#SBATCH --error=./log_more_distortion_new/${task}_chunk_${CHUNK_IDX}_error.txt
#SBATCH --job-name=${CHUNK_IDX}${task}

python batch_distortion_new_new.py \
    --chunk_num 32 \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done