#!/bin/bash

set -e

# installation of Mamba
export HOME=$PWD
export PATH
bash Miniforge3-Linux-x86_64.sh -b -p $PWD/miniforge3
export PATH=$PWD/miniforge3/bin:$PATH

# install packages
rm -rf $PWD/miniforge3/envs/*
conda init
mamba env create -f lammps.yml --force

# activate the environment
mamba activate lammps
signac init

# run script
