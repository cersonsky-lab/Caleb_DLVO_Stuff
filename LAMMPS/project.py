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
    return os.path.isfile(job.fn('data.lammps'))

@MyProject.label
def check_equilibrium(job):
    equilibrium = False

    from analyze import run_analysis
    run_analysis(job, job.fn('data.lammps'))

    if os.path.isfile(job.fn('equilibrium_data.txt')):
        equilibrium = True
    return equilibrium

# @MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from lammps import lammps
    # Copy the original LAMMPS input file to the job's directory
    shutil.copy("input.run.lammps", job.fn("input.run.lammps"))
    with job:
        # Read the original LAMMPS input script
        with open(job.fn("input.run.lammps"), "r") as f:
            original_script = f.read()

        # Prepend job-specific parameters to the original LAMMPS script
        added_params = (f"variable L equal {job.sp.L}\n"
                        f"variable N equal {job.sp.N}\n"
                        f"variable radius equal {job.sp.r}\n"
                        f"variable M1 equal {job.sp.M}\n"
                        f"variable epsilon_vdw equal {job.sp.epsilon}\n"
                        f"variable kappa equal {job.sp.kappa}\n"
                        f"variable Acc equal {job.sp.A}\n"
                        f"variable d1 equal {2*job.sp.r}\n"
                        f"variable T equal {job.sp.T}\n"
                        f"variable seed equal {job.sp.seed}\n"
                        f"variable steps equal {job.sp.steps}\n")

        # Write the modified LAMMPS script back to the file
        with open(job.fn("input.run.lammps"), "w") as f:
            f.write(added_params + original_script)

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
