#!/bin/bash
#SBATCH --account=mosoleyma_1026
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=1:30:00
module purge
module load gcc/11.3.0
module load python/3.9.12
python3 change_name.py