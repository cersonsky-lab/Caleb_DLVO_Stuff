import numpy as np
import sys
from signac import get_project
from matplotlib import pyplot as plt

# Tying script to Signac jobs
job_id = sys.argv[2]
project = get_project()
job = project.open_job(id=job_id)

# Function to find autocorrelation
def autocorrelation(data):
    normalized_data = (data - np.mean(data)) / (np.std(data) * len(data))
    autocorr = np.correlate(normalized_data, normalized_data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    return autocorr

equilibrium = False
equilibrium_data = []

# Generates data into readable arrays
arr = np.genfromtxt(sys.argv[1])
arr = np.delete(arr, 0, axis=0)
energy = arr[:,0]
timestep  = list(range(0, len(energy)*1000, 1000))
timestep = np.array(timestep).reshape(-1, 1)
arr = np.column_stack((arr, timestep))
pressure = arr[:,1]
temperature = arr[:,2]

# Plots energy and checks equilibrium status
plot = plt.plot(timestep, energy)
plt.scatter(timestep, energy)
plt.yscale('log')
plt.savefig(job.fn('E_plot.png'))
E_correlation = autocorrelation(energy)
print(E_correlation)

# Sweeps the sim 1000 data points at a time to find where (or if) equilibrium is reached
for segment in range(0, len(E_correlation), 10):
    E_segment = E_correlation[segment:segment+10]
    if np.all(E_segment<1E4) and equilibrium == False:
        equilibrium = True
        equilibrium_data = arr[segment:len(energy),:]
    elif not np.all(E_segment<1E4) and equilibrium == True:
        equilibrium = False
        equilibrium_data = []:
if len(equilibrium_data) == 0
    np.savetxt(job.fn('equilibrium_data.txt'), equilibrium_data)

