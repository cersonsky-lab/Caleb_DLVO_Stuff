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
conda env create -f project.yml
conda activate project
signac init

# any new jobs that need to be created (these are just examples)
signac job '{"seed": 1, "N_particles": 124, "L": 100, "kappa": 11.7, "A": 2.73, "Z": 0.0, "a1": 1, "a2": 1, "steps": 1e11, "rcut": 1}' --create


# initialize jobs
python project.py run
