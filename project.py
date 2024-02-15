from flow import FlowProject
import numpy as np
import os
import subprocess

class MyProject(FlowProject):
    pass

@MyProject.label
def ran(job):
    return os.path.isfile(job.fn('log.txt'))

@MyProject.label
def check_equilibrium(job):
    equilibrium = False
    job_log = job.fn('log.txt')
    subprocess.call(["python", "analyze.py", job_log, job.id])
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
