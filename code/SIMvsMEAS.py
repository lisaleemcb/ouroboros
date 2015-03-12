import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
#import mpld3
from IPython.display import Image

k_B = 1.381e-23 # Boltzmann constant (J/K)
Q_cav = 1000.
Q_1 = Q_cav
Q_2 = 2800.
Q_L = 1400. #1 / (1/Q_cav + 1/Q_1 + 1/Q_2)
omega_0 = 2.256e9
t_0 = 1 / 1.e9 # no phase delay, with phase delay t_0 = 1 / 1.e6
theta = 0 #set additional phase shift equal to 0

N_0 = 300. #kelvin
N_a = 300. #our amplifiers have a NF of 3 dB
N_b = 300. #not sure how to measure the backwards noise?

S = [[-1 + 2 * Q_L/Q_cav , 2 * Q_L/np.sqrt(Q_cav * Q_1) , 2 * Q_L/np.sqrt(Q_cav * Q_2)],
    [2 * Q_L/np.sqrt(Q_cav * Q_1), -1 + 2 * Q_L/Q_1, 2 * Q_L/np.sqrt(Q_1 * Q_2)],
    [2 * Q_L/np.sqrt(Q_cav * Q_2), 2 * Q_L/np.sqrt(Q_1 * Q_2), -1 + 2 * Q_L/Q_2]]

def active_Q(G):
    return 1 / (1/Q_L - 2 * np.sqrt(G) / np.sqrt(Q_1 * Q_2))

def output_power(G, Q, t):
    numer = S[1][0]**2 * N_0 + S[1][1]**2 * N_b + S[1][2]**2 * G * N_a
    denom = 1 + S[1][2]**2 * G - 2 * S[1][2] * np.sqrt(G) * np.exp( - omega_0 * t / Q)
    try:
        return numer / denom
    except Exception as e:
        raise Exception(str(e))

#MEASUREMENT VARIABLES
#-------------------------------------------------------------
fileMEAS6 = "MEAS6cutsort.txt"
fileMEAS7 = "MEAS7cutsort.txt"

MEAS6 = np.genfromtxt(fileMEAS6)
MEAS7 = np.genfromtxt(fileMEAS7)

#variables
voltagePS6 = MEAS6[:,0]
voltagePS7 = MEAS7[:,0]

voltagePhase6 = MEAS6[:,1]
voltagePhase7 = MEAS7[:,1]

freqVNA6 = MEAS6[:,2]
freqVNA7 = MEAS7[:,2]

Q6 = MEAS6[:,3]
Q7 = MEAS7[:,3]

noise6 = MEAS6[:,4]
noise7 = MEAS7[:,4]

signal6 = MEAS6[:,5]
signal7 = MEAS7[:,5]

logSNR6 = signal6 - noise6
logSNR7 = signal7 - noise7

linSNR6 = 10.0**(logSNR6/10.0)
linSNR7 = 10.0**(logSNR7/10.0)

linNoise6 = 10.0**((noise6)/10.0)
linNoise7 = 10.0**((noise7)/10.0)
#linNoiseTemp6a = linNoise6 / (1000*k_B*1e6)
#linNoiseTemp6b = linNoise6 / (1000*k_B*1e7)
linNoiseTemp6c = linNoise6 / (1000.*k_B*4e6)
linNoiseTemp6d = linNoise6 / (1000.*k_B*1e5)

linNoiseTemp7 = linNoise7 / 1000.*k_B*1e6
#linNoiseTemp7a = linNoise7 / (1000*k_B*1e6)
#linNoiseTemp7b = linNoise7 / (1000*k_B*1e7)
linNoiseTemp7c = linNoise7 / (1000.*k_B*4e6)
linNoiseTemp7d = linNoise7 / (1000.*k_B*1e5)

linSignal6 = 10.0**((signal6)/10.0)
linSignal7 = 10.0**((signal7)/10.0)

#PLOTTING
#-------------------------------------------------------------
gains = np.linspace(.01,7,50)
q_s = [active_Q(g) for g in gains]
t = [2.033e-9, 2.4e-6]
powers_nodelay = [output_power(g, q, t[0]) for g, q in zip(gains, q_s)]
powers_delay = [output_power(g, q, t[1]) for g, q in zip(gains, q_s)]


fig, (ax1, ax3) = plt.subplots(nrows=1, ncols=2)
#fig.set_size_inches(17.5,9)
fig.suptitle('Experimental data with tweakable parameter, overlaid on simulated data, Q_cav = 1000')

ax1.plot(q_s, powers_nodelay, 'ko', marker='$\circ$')
#ax1.plot(Q6, linNoiseTemp6a, 'ro')
#ax1.plot(Q6, linNoiseTemp6b, 'bo')
ax1.plot(Q6, linNoiseTemp6c, 'ro', label="perfect fudge factor of 4e6")
ax1.plot(Q6, linNoiseTemp6d, 'go', label="measured gain after AFR circuit of 1e5")
ax1.set_xlabel('Q')
ax1.set_ylabel('Noise (Kelvin)')
ax1.set_title('Noise vs Q for t = %.1e' % t[0])


#ax2.plot(S[1][2]**2 * gains, powers_nodelay, 'ko', marker='$\circ$')
#ax2.set_xlabel('Effective Gain $|S_{23}|^2 G$')
#ax2.set_ylabel('Noise (Kelvin)')
#ax2.set_title('Noise vs Voltage for t = %.1e' % t[0])

ax3.plot(q_s, powers_delay, 'ko', marker='$\circ$')
#ax3.plot(Q7, linNoiseTemp7a, 'ro')
#ax3.plot(Q7, linNoiseTemp7b, 'bo')
ax3.plot(Q7, linNoiseTemp7c, 'ro', label="perfect fudge factor of 4e6")
ax3.plot(Q7, linNoiseTemp7d, 'go', label="measured gain after AFR circuit of 1e5")
ax3.set_xlabel('Q')
ax3.set_ylabel('Noise (Kelvin)')
ax3.set_title('Noise vs Q for t = %.1e' % t[1])


#ax4.plot(S[1][2]**2 * gains, powers_delay, 'ko', marker='$\circ$')
#ax4.set_xlabel('Effective Gain $|S_{23}|^2 G$')
#ax4.set_ylabel('Noise (Kelvin)')
#ax4.set_title('Noise vs Voltage for t = %.1e' % t[1]);
#ax1.set_yscale('log')
#ax3.set_yscale('log')
plt.legend()
plt.show()
#fig.savefig('SIMvsMEAS.png')
