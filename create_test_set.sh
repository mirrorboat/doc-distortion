#!/bin/bash

task_list=(
    binarization
    # blur
    wrap
    shadow
)

CHUNK_NUM=1

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
#SBATCH --output=./log/testset/${task}_chunk_${CHUNK_IDX}_output_new.txt
#SBATCH --error=./log/testset/${task}_chunk_${CHUNK_IDX}_error_new.txt

python batch_distortion.py \
    --chunk_num ${CHUNK_NUM} \
    --chunk_idx ${CHUNK_IDX} \
    --distortion ${task} \
    --target_folder 20250130_testset
EOT
done
done