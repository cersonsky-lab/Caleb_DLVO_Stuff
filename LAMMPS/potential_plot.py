# Plot pair potentials from analytical equations

import numpy as np
import matplotlib.pyplot as plt

# Defining system parameters
Acc = 75.398      	    # Hamaker constant for colloid-colloid interaction
a1 = 1			    # radius of particle 1
a2 = 1                      # radius of particle 2
sigma_cc = 0.01        	    # Lennard-Jones distance constant (for colloid particle?)
A_ykw = 100                 # prefactor in Yukawa potential
kappa = 2		    # inverse screening length
# for low surf potential, A=2pi * R * epsilon*eplison0 * kappa * surface potential.
em = 12.0                   # dielectric constant of the medium (EMIM TFSI, 25degreeC)
e0 = 8.854188 * 10**(-12)   # vacuum permittivity (F m-1)
e = 1.60217663 * 10**(-19)  # elementary charge (C)
kT = 0.1                    # temperature term
ys = 0.04                   # reduced surface potential (scaled by kT/e)


r = np.arange(1.001*(a1+a2), 1.1*(a1+a2)+5, 0.005)

# Interaction derived from Lennard-Jones
def UA(r):
    UA = -Acc / 6 * (2 * a1 * a2 / (r ** 2 - (a1 + a2) ** 2) + 2 * a1 * a2 / (r ** 2 - (a1 - a2) ** 2) + np.log(
        (r ** 2 - (a1 + a2) ** 2) / (r ** 2 - (a1 - a2) ** 2)))
    return UA

def UR(r):
    UR = Acc / 37800 * sigma_cc ** 6 / r * (
            (r ** 2 - 7 * r * (a1 + a2) + 6 * (a1 ** 2 + 7 * a1 * a2 + a2 ** 2)) / (r - a1 - a2) ** 7 +
            (r ** 2 + 7 * r * (a1 + a2) + 6 * (a1 ** 2 + 7 * a1 * a2 + a2 ** 2)) / (r + a1 + a2) ** 7 -
            (r ** 2 + 7 * r * (a1 - a2) + 6 * (a1 ** 2 - 7 * a1 * a2 + a2 ** 2)) / (r + a1 - a2) ** 7 -
            (r ** 2 - 7 * r * (a1 - a2) + 6 * (a1 ** 2 - 7 * a1 * a2 + a2 ** 2)) / (r - a1 + a2) ** 7)
    return UR

def LJ(r):
    U = UA(r) + UR(r)
    return U


# Yukawa potential for colloid
def Yukawa(r):
    E = A_ykw/kappa * np.exp(-kappa * (r-(a1+a2)))
    return E

def elec_new(r):
    Y = 4*np.exp(-kappa*(r-2*a1)/2)*np.arctanh(np.exp(-kappa*(r-2*a1)/2) * np.tanh(ys/4))
    E = em * e0 * (kT/e)**2 * Y * (a1**2 /r) * np.log(1+np.exp(-kappa*(r-2*a1)))
    return E


# Plot
plt.plot(r, LJ(r), color='black', label='LJ-like potential')
plt.plot(r, UA(r), color='red', label='vdW attraction', linestyle='--')
plt.plot(r, UR(r), color='blue', label='LJ repulsion', linestyle='--')
plt.ylim([np.floor(np.min(LJ(r))), min(np.max(LJ(r)),3)])
plt.title('LJ-like potential: Acc='+str(Acc))
plt.xlabel('r')
plt.ylabel('potential')
plt.grid()
plt.legend()
plt.show()

plt.figure()
plt.plot(r, Yukawa(r), label='Yukawa potential')
plt.title('Yukawa potential: Ay='+str(A_ykw))
plt.xlabel('r')
plt.ylabel('potential')
plt.show()


DLVO = LJ(r)+Yukawa(r)
plt.figure()
plt.plot(r, LJ(r), color='blue', label='LJ-like potential', linestyle='--')
plt.plot(r, Yukawa(r), color='red', label='Yukawa potential', linestyle='--')
plt.plot(r, DLVO, color='black', label='DLVO potential')
plt.title('DLVO potentials: Acc='+str(Acc)+' Ay='+str(A_ykw))
plt.xlabel('r')
plt.ylabel('potential')
plt.ylim([np.floor(np.min(LJ(r)))-2, -np.floor(np.min(LJ(r)))])
plt.grid()
plt.legend()
plt.show()

# plt.figure()
# plt.plot(r, UA(r), color='blue', label='LJ-like potential', linestyle='--')
# plt.plot(r, Yukawa(r), color='red', label='Yukawa potential', linestyle='--')
# plt.plot(r, UA(r)+Yukawa(r), color='black', label='DLVO potential')
# plt.title('DLVO potentials: Acc='+str(Acc)+' Ay='+str(A_ykw))
# plt.xlabel('r')
# plt.ylabel('potential')
# plt.ylim([np.floor(np.min(LJ(r)))-2, 5])
# plt.legend()
# plt.show()
"""

plt.figure()
plt.plot(r, elec_new(r), label='electrostatic potential')
plt.title('Electrostatic potential')
plt.xlabel('r')
plt.ylabel('potential')
plt.show()
"""
