# -*- coding: utf-8 -*-
"""
COMPUTE THE RADIAL DISTRIBUTION FUNCTION FOR A MIXTURE OF TWO PARTICLES.
In this case we only consider the contribution of the distances between particles of equal type.

The script is adapted for compute the rdf from the output of LAMMPS.

run: >> python rdf_xx.py arg
arg is the file where the positions of particles are stored.

Author: DiegoDZ
"""


def rdf(S, rMax, nbin, arg):

    import numpy as np

    # Load the position file.
    f = np.loadtxt(str(arg))
    # Number of particles.
    npart = 256
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

    for a in range(0,number_timesteps + size_snapshot, size_snapshot):
        h=f[np.where(f[:,7] == a)] # Column 7 indicates the snapshot where we are.
        # Select the corresponding columns for the position x, y, z.
        x = h[:,2]
        y = h[:,3]
        z = h[:,4]
        for i in range(npart-1):
            for j in range(i+1, npart):
                    xr = x[i] - x[j]
                    yr = y[i] - y[j]
                    zr = z[i] - z[j]
                    # Get the closer image.
                    xr = xr - S*round(xr/S)
                    yr = yr - S*round(yr/S)
                    zr = zr - S*round(zr/S)
                    # Compute the distance.
                    d = np.sqrt(xr*xr + yr*yr + zr*zr)
                    # Select the bin.
                    bin = int(d/dr)
                    if bin <= nbin-1:
                        g[bin] = g[bin] + 2.0 # Contribution for particle i and j.

    # Normalize g
    const = 4.0 * np.pi * den_part / 3.0
    for i in range(nbin):
        rlower = float(i) * dr
        rupper = rlower + dr
        nideal = const * (rupper ** 3 - rlower ** 3)
        g[i] = g[i] / npart / nideal / count
        r[i] = (rupper + rlower) / 2
    return g,r


import sys
import numpy as np

(g,r) = rdf(36.4554, 15, 150, sys.argv[1])
#print r,g

#import matplotlib.pyplot as plt
#plt.plot(r,g)
#plt.show()


# The next piece of code is to obtain the output in the desired format.
out = np.array([r,g]).T
aux = ''
for line in out:
    for element in line:
        aux = aux + str(element) + ' '
    aux = aux + '\n'

print aux

# EOF
