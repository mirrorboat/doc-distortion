#!/bin/bash

json_ls=(
    /mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_first_second_sampling/all_1_bigger_distortion.json
    /mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_first_second_sampling/all_2_bigger_distortion.json
    /mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_first_second_sampling/all_3_bigger_distortion.json
    /mnt/petrelfs/chenjingzhou/cjz/doc-distortion/meta_data_subset_first_second_sampling/all_4_bigger_distortion.json
)

CHUNK_NUM=16

# for json_path in ${json_ls[@]}
# 加上递增的idx
for idx in $(seq 0 $(( ${#json_ls[@]} - 1 )))
do
json_path=${json_ls[$idx]}
for CHUNK_IDX in $(seq 0 $((CHUNK_NUM - 1)))
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --output=./log_s2write2/${idx}_${CHUNK_IDX}_output.txt
#SBATCH --error=./log_s2write2/${idx}_${CHUNK_IDX}_error.txt
#SBATCH --job-name=upl

python s3_write2.py \
    --json_file_path ${json_path} \
    --chunk_num ${CHUNK_NUM} \
    --chunk_id ${CHUNK_IDX} \
            
echo "done"
EOT
done
done