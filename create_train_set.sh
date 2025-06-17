#!/bin/bash

task_list=(
    # binarization
    # blur
    # wrap
    # shadow
    none
)

CHUNK_NUM=32

for task in ${task_list[@]}
do
for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
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
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done
done