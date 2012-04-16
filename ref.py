import numpy as np

#[eV]

#M. K. Bahl, R. L. Watson, and K. J. Irgolic, ChemPhys 68
TePeaks=np.array([481.6,483.9,485.3,491.8,493.9])

#AES Handbook, Pamberg, Riach, Weber, McDonald 1972
#negative derivative peaks at 96, 101, assume width 0.5 eV
BiPeaks=np.array([95.5,100.5])

#negative derivative peaks at 326, 330. Derivative doesn't reach 0 between them.
PdPeaks=np.array([325.5,329.0])
