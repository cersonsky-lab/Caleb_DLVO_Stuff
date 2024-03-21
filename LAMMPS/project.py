from flow import FlowProject
import numpy as np
import os
import subprocess
import shutil

class MyProject(FlowProject):
    pass

@MyProject.post.isfile('potential.png')
@MyProject.operation
def output_potential(job):
    from analyze import DLVO
    from matplotlib import pyplot as plt
    rs = np.linspace(0, 10, 100)
    plt.plot(rs, DLVO(job, rs))
    plt.savefig(job.fn('potential.png'))

@MyProject.label
def ran(job):
    return os.path.isfile(job.fn('run.data'))

@MyProject.label
def check_equilibrium(job):
    equilibrium = False

    from analyze import run_analysis
    run_analysis(job, job.fn('run.data'))

    if os.path.isfile(job.fn('equilibrium_data.txt')):
        equilibrium = True
    return equilibrium

@MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from lammps import lammps
    with job:
        # Copy the original LAMMPS input file to the job's directory
        shutil.copy("input.run.lammps", job.fn("input.run.lammps"))

        # Write parameters to the LAMMPS input script
        with open(job.fun("input.run.lammps"), "a") as f:
            f.write(f"variable L equal {job.sp.L}\n")
            f.write(f"variable N equal {job.sp.N}\n")
            f.write(f"variable radius equal {job.sp.r}\n")
            f.write(f"variable M1 equal {job.sp.M}\n")
            f.write(f"variable epsilon_vdw equal {job.sp.epsilon}\n")
            f.write(f"variable kappa equal {job.sp.kappa}\n")
            f.write(f"variable Acc equal {job.sp.A}\n")
            f.write(f"variable d1 equal {2*job.sp.r}\n")
            f.write(f"variable T equal {job.sp.T}\n")
            f.write(f"variable seed equal {job.sp.seed}\n")
            f.write(f"variable steps equal {job.sp.steps}\n")

        # Run the LAMMPS script
        lmp = lammps()
        lmp.file(job.fn("input.run.lammps"))

# Ignoring for now
# @MyProject.pre(ran)
# @MyProject.post(check_equilibrium)
# @MyProject.operation
# def continue_mc(job):
#     from input.run import resume
#     with job:
#         resume(job)

if __name__=="__main__":
    MyProject().main()
