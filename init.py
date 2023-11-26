import signac

project = signac.init_project()

import itertools
import math

import gsd.hoomd
import hoomd
import numpy as np
from hoomd import hpmc, md


def simulate(job):
    device = hoomd.device.CPU()
    sim = hoomd.Simulation(device=device)
    sim.seed = job.sp.seed

    N_particles = job.sp.N_particles
    L = job.sp.L

    K = math.ceil(N_particles ** (1 / 3))
    x = np.linspace(-L / 2, L / 2, K, endpoint=False)
    position = list(itertools.product(x, repeat=3))

    snapshot = gsd.hoomd.Frame()
    snapshot.particles.N = N_particles
    snapshot.particles.types = ["A","B"]
    snapshot.particles.position = position[0:N_particles]
    snapshot.particles.typeid = np.repeat([0, 1], N_particles // 2)
    np.random.shuffle(snapshot.particles.typeid)
    snapshot.configuration.box = [L, L, L, 0, 0, 0]

    sim.create_state_from_snapshot(snapshot)

    with gsd.hoomd.open(name="lattice.gsd", mode="w") as f:
        f.append(snapshot)

    # Set up the neighbor list
    nlist = md.nlist.Cell(buffer=0.5)

    # Define DLVO potential
    dlvo = md.pair.DLVO(nlist=nlist, default_r_cut=1.0)

    dlvo.params["A", "A"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)
    dlvo.params["A", "B"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)
    dlvo.params["B", "B"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)

    # Integrate
    integrator = md.Integrator(dt=0.0005)
    integrator.forces.append(dlvo)

    langevin = md.methods.Langevin(kT=1.0, filter=hoomd.filter.All())
    integrator.methods.append(langevin)
    sim.operations.integrator = integrator

    trigger = hoomd.trigger.Periodic(period=int(1E3))

    # Log data
    logger = hoomd.logging.Logger(categories=["scalar", "string"])
    table = hoomd.write.Table(trigger=trigger, logger=logger)

    # Create a ThermodynamicQuantities object for the simulation
    thermo = hoomd.md.compute.ThermodynamicQuantities(filter=hoomd.filter.All())
    sim.operations.computes.append(thermo)

    # Add a log for the tracked variables
    logger.add(thermo, quantities=['kinetic_energy','pressure','kinetic_temperature'])

    # Log during sim (not running with CHTC)
    # sim.operations.writers.append(table)


    # Save results to table
    file = open("log.txt", mode="w", newline="\n")
    table_file = hoomd.write.Table(
        output=file, trigger=trigger, logger=logger
    )
    sim.operations.writers.append(table_file)

    gsd_writer = hoomd.write.GSD(filename='trajectory.gsd',
            trigger=trigger)

    sim.operations.writers.append(gsd_writer)

    # Run simulation
    sim.run(job.sp.steps)

def resume(job)
    device = hoomd.device.CPU()
    sim = hoomd.Simulation(device=device)

    # Takes the old starting point as the resuming point
    gsd.hoomd.open(filename='trajectory.gsd','rb') as f:
        snapshot = f[-1]
    sim.create_state_from_snapshot(snapshot)

    # Set up the neighbor list
    nlist = md.nlist.Cell(buffer=0.5)

    # Define DLVO potential
    dlvo = md.pair.DLVO(nlist=nlist, default_r_cut=1.0)

    dlvo.params["A", "A"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)
    dlvo.params["A", "B"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)
    dlvo.params["B", "B"] = dict(A=job.sp.A, kappa=job.sp.kappa, Z=job.sp.Z, a1=job.sp.a1, a2=job.sp.a2)

    # Integrate
    integrator = md.Integrator(dt=0.0005)
    integrator.forces.append(dlvo)

    langevin = md.methods.Langevin(kT=1.0, filter=hoomd.filter.All())
    integrator.methods.append(langevin)
    sim.operations.integrator = integrator

    trigger = hoomd.trigger.Periodic(period=int(1E3))

    # Log data
    logger = hoomd.logging.Logger(categories=["scalar", "string"])
    table = hoomd.write.Table(trigger=trigger, logger=logger)

    # Create a ThermodynamicQuantities object for the simulation
    thermo = hoomd.md.compute.ThermodynamicQuantities(filter=hoomd.filter.All())
    sim.operations.computes.append(thermo)

    # Add a log for the tracked variables
    logger.add(thermo, quantities=['kinetic_energy','pressure','kinetic_temperature'])

    # Save results to table
    file = open("log.txt", mode="a", newline="\n")
    table_file = hoomd.write.Table(
        output=file, trigger=trigger, logger=logger
    )
    sim.operations.writers.append(table_file)

    gsd_writer = hoomd.write.GSD(filename='trajectory.gsd',
            trigger=trigger, mode='ab')

    sim.operations.writers.append(gsd_writer)

    # Run simulation
    sim.run(job.sp.steps)

