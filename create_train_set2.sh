#!/bin/bash

task_list=(
    # binarization
    # blur
    # wrap
    # shadow
    none
)

CHUNK_NUM=8

for task in "${task_list[@]}"
do
    for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
    do
        nohup srun --partition=s2_bigdata --nodes=1 --ntasks=1 --cpus-per-task=1 \
            python batch_distortion.py \
                --chunk_num "${CHUNK_NUM}" \
                --chunk_idx "${CHUNK_IDX}" \
                --distortion "${task}" \
            > "./log/${task}_chunk_${CHUNK_IDX}.log" 2>&1 &
        sleep 5
    done
done