#!/bin/bash

task_list=(
    binarization
    blur
    wrap
    shadow
    none
)

CHUNK_NUM=4

for task in ${task_list[@]}
do
for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=./log_more_distortion_new2/${task}_chunk_${CHUNK_IDX}_output.txt
#SBATCH --error=./log_more_distortion_new2/${task}_chunk_${CHUNK_IDX}_error.txt
#SBATCH --job-name=${CHUNK_IDX}${task}

python batch_distortion_new_new.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done
done