import os
import numpy as np
import sys
from matplotlib import pyplot as plt


def analyze(job):
    job_log = job.fn("log.txt")

    # Function to find autocorrelation
    def autocorrelation(data):
        normalized_data = (data - np.mean(data)) / (np.std(data) * len(data))
        autocorr = np.correlate(normalized_data, normalized_data, mode="full")
        autocorr = autocorr[len(autocorr) // 2 :]
        return autocorr

    equilibrium_data = []

    # Generates data into readable arrays
    arr = np.genfromtxt(job_log)
    arr = np.delete(arr, 0, axis=0)
    energy = arr[:, 0]
    timestep = list(range(0, len(energy) * 1000, 1000))
    timestep = np.array(timestep).reshape(-1, 1)
    arr = np.column_stack((arr, timestep))
    pressure = arr[:, 1]
    temperature = arr[:, 2]

    # Plots energy and checks equilibrium status
    plot = plt.plot(timestep, energy)
    plt.scatter(timestep, energy)
    plt.savefig(job.fn("E_plot.png"))
    E_correlation = autocorrelation(energy)

    # Sweeps the sim 1000 data points at a time to find where (or if) equilibrium is reached
    for segment in range(0, len(E_correlation), 100):
        E_segment = E_correlation[segment : segment + 100]
        if np.argmax(E_segment) == len(E_segment) // 2 and not job.document.get(
            "equilibrium", False
        ):
            job.document["equilibrium"] = True
            equilibrium_data = arr[segment : len(energy), :]
        elif np.argmax(E_segment) != len(E_segment) // 2 and job.document.get(
            "equilibrium", False
        ):
            job.document["equilibrium"] = False
            equilibrium_data = []
    if equilibrium_data != []:
        np.savetxt(job.fn("equilibrium_data.txt"), equilibrium_data)
