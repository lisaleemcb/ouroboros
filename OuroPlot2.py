import cmath
import numpy as np
import matplotlib.pyplot as plt


#variable initialization
T_o = 1  # in units (K)
T_a = 1  # (K)
T_b = 1  # (K)
B_o = 1
B_a = 1
B_c = 1
phi_1 = 0
phi_2 = np.pi / 2
phi_3 = np.pi
G = np.linspace(0, 5)

#function initialization
#correlated noise
T_n1_corr = ((T_o + T_a * G * B_a) * B_c)/(abs(1 - np.sqrt(G) * cmath.exp(1j*phi_1))**2)
T_n2_corr = ((T_o + T_a * G * B_a) * B_c)/(abs(1 - np.sqrt(G) * cmath.exp(1j*phi_2))**2)
T_n3_corr = ((T_o + T_a * G * B_a) * B_c)/(abs(1 - np.sqrt(G) * cmath.exp(1j*phi_3))**2)
corrGray = 1/(1 - np.sqrt(G))**2

#uncorrelated noise
T_n_uncorr = B_o * T_o + ((B_a - B_c * np.sqrt(G))**2) * T_b + (B_c**2) * G * T_a
uncorrGray = 1/(1-G)

plt.plot(G, T_n2_corr, linewidth=2.5, linestyle="-", label=r'$Italian \phi=\frac{\pi}{2}$' )
plt.plot(G, T_n3_corr, linewidth=2.5, linestyle="-", label=r'$Italian\ \phi=\pi$' )
plt.plot(G, T_n_uncorr, linewidth=2.5, linestyle="-", label='$Japanese$')
plt.plot(G, corrGray, linewidth=2.5, linestyle="--", label='$ 1/(1-\sqrt{G})^{2} $')
plt.plot(G, uncorrGray, linewidth=2.5, linestyle="--", label='$ 1/(1-G) $')

plt.ylim((0,5))
plt.yscale('linear')
plt.ylabel('Noise Temperature')
plt.xlabel('Gain')
plt.legend(loc='upper right',borderaxespad=1)

plt.show()

