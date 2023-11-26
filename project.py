from flow import FlowProject
import numpy as np
import os

class MyProject(FlowProject):
    pass

@MyProject.label
def ran(job):
    return os.path.isfile(job.fn('log.txt'))

@MyProject.label
def check_equilibrium(job):
    equilibrium = False
    job_log = job.fn('log.txt')
    subprocess.call(["python", "analyze.py", job_log])
    return equilibrium

@MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from init import simulate
    with job:
        simulate(job)

if __name__=="__main__":
    MyProject().main()

@MyProject.pre(ran)
@MyProject.post(check_equilibrium)
def continue_mc(job)
    from init import resume
    with job:
        resume(job)
