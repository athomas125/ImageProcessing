#!/bin/bash

# See https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0041998 for slurn usage details
# List of folders to process
FOLDERS=("YH_s1_tr1_BowerBuilding" "YH_s1_tr2_BowerBuilding" "YH_s2_tr1_BowerBuilding" 
         "YH_s2_tr2_BowerBuilding" "YH_s3_tr1_BowerBuilding" "YH_s4_tr1_BowerBuilding" 
         "YH_s5_tr1_BowerBuilding" "YH_s6_tr1_BowerBuilding" "YH_s7_tr1_BowerBuilding" 
         "YH_s7_tr2_BowerBuilding" "YH_s7_tr3_BowerBuilding")

# Iterate over each folder and submit a job
for FOLDER in "${FOLDERS[@]}"; do
    sbatch <<EOT
#!/bin/bash
#SBATCH -JSlurmProcessVideo
#SBATCH --account=gts-coc-coda20
#SBATCH --mail-type=ALL
#SBATCH --mail-user=athomas314@gatech.edu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4G
#SBATCH -qinferno
#SBATCH --output=Report_%A-%a.out
#SBATCH --time=24:00:00

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Conda initialization
__conda_setup="\$('/usr/local/pace-apps/manual/packages/anaconda3/2022.05.0.1/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ \$? -eq 0 ]; then
    eval "\$__conda_setup"
else
    if [ -f "/usr/local/pace-apps/manual/packages/anaconda3/2022.05.0.1/etc/profile.d/conda.sh" ]; then
        . "/usr/local/pace-apps/manual/packages/anaconda3/2022.05.0.1/etc/profile.d/conda.sh"
    else
        export PATH="/usr/local/pace-apps/manual/packages/anaconda3/2022.05.0.1/bin:\$PATH"
    fi
fi
unset __conda_setup

# Activate the conda environment
conda activate IMG_PROC

# Add rclone to PATH
export PATH=\$PATH:/storage/coda1/d-coc/0/athomas314/rclone/rclone-v1.66.0-linux-amd64

# Set the JUST_FOLDERS variable for this job
export JUST_FOLDERS=${FOLDER}

# Call the python script with the specified folder
python /storage/home/hcoda1/0/athomas314/ondemand/CichlidBowerTracking/ImageProcessing/src/pull_and_process.py
EOT
done