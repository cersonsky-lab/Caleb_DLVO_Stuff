from flow import FlowProject
import numpy as np
import os
from analyze import analyze


class MyProject(FlowProject):
    pass


@MyProject.label
def ran(job):
    return os.path.isfile(job.fn("log.txt"))


@MyProject.label
def check_equilibrium(job):
    analyze(job)
    return job.document.get("equilibrium")


@MyProject.post(ran)
@MyProject.operation
def run_mc(job):
    from init import simulate

    with job:
        simulate(job)


@MyProject.pre(ran)
@MyProject.post(check_equilibrium)
def continue_mc(job):
    from init import resume

    with job:
        resume(job)


if __name__ == "__main__":
    MyProject().main()
