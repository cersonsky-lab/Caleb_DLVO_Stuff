#!/bin/bash

# save job exit if any command returns with non-zero exit status (aka failure)
set -e

# installation steps for Miniconda
export HOME=$PWD
export PATH
bash Miniconda3-latest-Linux-x86_64.sh -b -p $PWD/miniconda3
export PATH=$PWD/miniconda3/bin:$PATH

# install packages
rm -rf $PWD/miniconda3/envs/*
source $PWD/miniconda3/etc/profile.d/conda.sh
conda env create -f DLVO.yml
conda activate DLVO
signac init

# any new jobs that need to be created

# initialize jobs
python project.py run
