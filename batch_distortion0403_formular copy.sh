#!/bin/bash

task_list=(
    # binarization
    blur
    # warp
    # shadow
)
CHUNK_NUM=16

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
#SBATCH --output=./log0403/formular/${task}_${CHUNK_IDX}_${CHUNK_NUM}_output.txt
#SBATCH --error=./log0403/formular/${task}_${CHUNK_IDX}_${CHUNK_NUM}_error.txt
#SBATCH --job-name=${CHUNK_IDX}${task}

python batch_distortion0403_formular.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \

EOT
done
done