from flow import FlowProject
import numpy as np
import os
import subprocess
import lammps

class MyProject(FlowProject):
    pass

def run_lammps(job):
    lmp = lammps()
    lmp.file(job.fn('simulate.lammps'))  # Read LAMMPS input file
    lmp.command("run 10000")  # Run simulation for 10000 steps

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
    with job:
        run_lammps(job)

@MyProject.pre(ran)
@MyProject.post(check_equilibrium)
@MyProject.operation
def continue_mc(job):
    with job:
        run_lammps(job)

if __name__=="__main__":
    MyProject().main()
