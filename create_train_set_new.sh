#!/bin/bash

task_list=(
    # binarization
    # blur
    # wrap
    # shadow
    none
)

CHUNK_NUM=16

for task in ${task_list[@]}
do
for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=s2_bigdata
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=./log_more_distortion/${task}_chunk_${CHUNK_IDX}_output.txt
#SBATCH --error=./log_more_distortion/${task}_chunk_${CHUNK_IDX}_error.txt
#SBATCH --job-name=n${task}${CHUNK_IDX}

python batch_distortion_new.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done
done