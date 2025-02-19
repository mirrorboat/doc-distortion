#!/bin/bash

task_list=(
    # binarization
    blur
    # wrap
    # shadow
)

for task in ${task_list[@]}
do
    sbatch <<EOT
#!/bin/bash
#SBATCH --partition=new_cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --output=./existence_log/${task}_existetence_output.txt   # 标准输出文件
#SBATCH --error=./existence_log/${task}_existetence_error.txt     # 错误输出文件

python check_image_existetence.py --distortion ${task}
EOT
done