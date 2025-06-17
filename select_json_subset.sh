#!/bin/bash

task_list=(
    binarization
    blur
    wrap
    shadow
    none
)

for task in ${task_list[@]}
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --output=./tmp/${task}_output.txt   # 标准输出文件
#SBATCH --error=./tmp/${task}_error.txt     # 错误输出文件

# python batch_distortion.py --distortion ${task}
python select_json_subset.py --distortion ${task}
EOT
done