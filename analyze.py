import numpy as np
import sys
from signac import get_project
from matplotlib import pyplot as plt

# Function to find autocorrelation
def autocorrelation(data):
	normalized_data = (data - np.mean(data)) / (np.std(data) * len(data))
	autocorr = np.correlate(normalized_data, normalized_data, mode='full')
	autocorr = autocorr[len(autocorr)//2:]
	return autocorr

def DLVO(job, r):
	return -1*(job.sp.A/6)*((2*job.sp.a1*job.sp.a2)/(r**2-(job.sp.a1+job.sp.a2)**2)+(2*job.sp.a1*job.sp.a2)/(r**2-(job.sp.a1-job.sp.a2)**2)+np.log((r**2-(job.sp.a1+job.sp.a2)**2)/(r**2-(job.sp.a1-job.sp.a2)**2)))+((job.sp.a1*job.sp.a2)/(job.sp.a1+job.sp.a2))*job.sp.Z*np.exp(-1*job.sp.kappa*(r-(job.sp.a1+job.sp.a2)))

def run_analysis(job, log):
	equilibrium = False
	equilibrium_data = []
	
	# Generates data into readable arrays
	arr = np.genfromtxt(log)
	arr = np.delete(arr, 0, axis=0)
	PE = arr[:,0]
	timestep = list(range(0, len(PE)*1000, 1000))
	timestep = np.array(timestep).reshape(-1, 1)
	arr = np.column_stack((arr, timestep))
	KE = arr[:,1]
	pressure = arr[:,2]
	temperature = arr[:,3]
	
	# Plots energy and checks equilibrium status
	plt.plot(timestep, PE)
	plt.scatter(timestep, PE)
	plt.yscale('linear')
	plt.title('Potential Energy vs. Time')
	plt.ylabel('Potential Energy [kT]')
	plt.xlabel('Time [steps]')
	plt.savefig(job.fn('E_plot.png'))
	plt.close()
	plt.yscale('linear')
	PE_correlation = autocorrelation(PE)
	
	# Sweeps the sim 1000 data points at a time to find where (or if) equilibrium is reached
	for segment in range(0, len(PE_correlation), 10):
		PE_segment = PE_correlation[segment:segment+10]
		if np.all(PE_segment<0.001) and np.all(PE_segment>-0.001) and equilibrium == False:
			equilibrium = True
			equilibrium_data = arr[segment:len(PE),:]
		elif (np.all(PE_segment>0.001) or np.all(PE_segment<-0.001)) and equilibrium == True:
			equilibrium = False
			equilibrium_data = []
	if len(equilibrium_data) != 0:
		np.savetxt(job.fn('equilibrium_data.txt'), equilibrium_data)
