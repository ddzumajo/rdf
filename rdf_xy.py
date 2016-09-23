# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
COMPUTE THE RADIAL DISTRIBUTION FUNCTION FOR A MIXTURE OF TWO PARTICLES.
In this case we only consider the contribution of the distances between particles of different type.

The script is adapted for compute the rdf from the output of LAMMPS.

run: >> python rdf_xy.py arg1 arg2
arg1 and arg2 are the files where the positons of particles are stored.

Author: DiegoDZ
"""


def rdf(S, rMax, nbin, arg1, arg2):

    import numpy as np

    # Load the positions file of two elements.
    f1 = np.loadtxt(str(arg1))
    f2 = np.loadtxt(str(arg2))
    # Number of particles of each element.
    npart1 = 256
    npart2 = 256
    npart = npart1 + npart2
    # Particle density (particle per volume).
    den_part = npart/ S**3
    # Bin size.
    dr = rMax/float(nbin)
    # Create an array 'r' with length the number of bines.
    r = np.zeros(nbin)
    # Create an array 'g' with length the number of bines.
    g = np.zeros(nbin)
    # The variables r and g will be the output of the program.

    # Number timesteps the LAMMPS simulation done.
    number_timesteps = 2000000
    # Number of timesteps the LAMMPS simulation done between snapshots.
    size_snapshot = 1000
    # Compute the number of snapshot using number_timesteps and size_snapshot.
    count = (number_timesteps / size_snapshot) + 1
    # Added +1 because the simulation started when timestep=0 and ended when timesteps=2000000

    # Now we compute the radial distribution function, g.
    # 1. For each snapshot we compute the distance between particles.
    # 2. For each distance computed we have to select the corresponding bin.
    #    When the bin was selected, we will add two (because there are two particles separated by that distance).
    #    We proceed in this way for all particles.

    for a in range(0,number_timesteps + size_snapshot,size_snapshot):
        h1 = f1[np.where(f1[:,7] == a)] # Column 7 indicates the snapshot where we are.
        # Select the corresponding columns for the position x, y, z.
        x1 = h1[:,2]
        y1 = h1[:,3]
        z1 = h1[:,4]
        # The same for the other file of positions.
        h2 = f2[np.where(f2[:,7] == a)]
        x2 = h2[:,2]
        y2 = h2[:,3]
        z2 = h2[:,4]
        for i in range(npart1):
            for j in range(npart2):
                    xr = x1[i] - x2[j]
                    yr = y1[i] - y2[j]
                    zr = z1[i] - z2[j]
                    # Get the closer image. (Periodic boundary conditions)
                    xr = xr - S*round(xr/S)
                    yr = yr - S*round(yr/S)
                    zr = zr - S*round(zr/S)
                    # Compute the distance.
                    d = np.sqrt(xr*xr + yr*yr + zr*zr)
                    # Select the bin.
                    bin = int(d/dr)
                    if bin <= nbin-1:
                        g[bin] = g[bin] + 2.0   # Contribution for particle i and j.

    # Normalize g
    const=4.0 * np.pi * den_part / 3.0
    for i in range(nbin):
        rlower = float(i) * dr
        rupper = rlower + dr
        nideal = const * (rupper ** 3 - rlower ** 3)
        g[i] = g[i] / npart1 / count / nideal
        r[i] = (rupper + rlower) / 2
    return g,r

import sys
import numpy as np

(g,r) = rdf(36.4554, 15, 150, sys.argv[1], sys.argv[2])
#print r,g

#import matplotlib.pyplot as plt
#plt.plot(r,g)
#plt.show()

# The next piece of code is to obtain the output with the desired format.
out = np.array([r,g]).T
aux = ''
for line in out:
    for element in line:
        aux = aux + str(element) + ' '
    aux = aux + '\n'

print aux


# EOF
