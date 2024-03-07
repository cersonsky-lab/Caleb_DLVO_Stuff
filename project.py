from flow import FlowProject
import numpy as np
import os
import subprocess

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
    return os.path.isfile(job.fn('log.txt'))

@MyProject.label
def check_equilibrium(job):
    equilibrium = False

    from analyze import run_analysis
    run_analysis(job, job.fn('log.txt'))

    if os.path.isfile(job.fn('equilibrium_data.txt')):
        equilibrium = True
    return equilibrium

@MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from simulate import init
    with job:
        init(job)

@MyProject.pre(ran)
@MyProject.post(check_equilibrium)
@MyProject.operation
def continue_mc(job):
    from simulate import resume
    with job:
        resume(job)

if __name__=="__main__":
    MyProject().main()
