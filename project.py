from flow import FlowProject
import numpy as np
import os

class MyProject(FlowProject):
    pass

def ran(job):
    return os.path.isfile(job.fn('log.txt'))


@MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from init import simulate
    with job:
        simulate(job)

if __name__=="__main__":
    MyProject().main()
