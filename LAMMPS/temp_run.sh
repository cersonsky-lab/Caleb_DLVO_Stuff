# Run lammps with OpenMP

# OMP_NUM_THREADS = 1
# export OMP_NUM_THREADS
lmp -in input.run.lammps -sf omp -pk omp 4
# mpirun -np 4 lmp_mpi -var f tmp.out -log nve_0.log -screen none -in input.run.lammps
