
# coding: utf-8

# In[64]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from IPython.display import Image
import numpy as np
from sympy.interactive import printing
printing.init_printing(use_latex=True)
Image(filename='afr_circuit.png')


# This code will compare simulation results for the Active Feedback Resonator (depicted above) with measurements.
# 
# The main output will be modeling the predicted behavior of the noise and snr vs Q in the case of coherent and incoherent noise.
# 
# Table of Contents:
# 
# [Theory](#theory)
# 
# [Simulations](#simulations)
# 
# [Measurements](#measurements)
# 
# [Comparison](#comparison)
# 
# [Literature Review](#literature)

### Theory <a id='theory'></a>

# Referencing the image above, we use the following notation: $N_0$ is the cavity thermal noise power, $N_b$ is the amplifier noise power traveling away from the amplifier, and $N_a$ is the noise power traveling towards the amplifier (referenced to the input of the amplifier). I use lower case to denote the respective voltages, so $n_0$ is the cavity voltage noise, and $|n_0|^2 = N_0$, etc. $\sqrt{G}$ is the voltage gain of the amplifier, with the effective gain of the circuit is given by $\sqrt{G}S_{23}$. The relationship between the input amplitudes $a$ and output amplitudes $b$ is given by the S parameter matrix:
# 
# $$
# S = \left(\begin{array}{ccc}
# -1 + 2Q_L/Q_{00} & 2 Q_L/\sqrt{Q_{00}Q_{1}} & 2Q_L/\sqrt{Q_{00} Q_2} \\
# 2 Q_L/\sqrt{Q_{00}Q_{1}} & -1 + 2Q_L/Q_{1} & 2Q_L/\sqrt{Q_{1} Q_2} \\
# 2 Q_L/\sqrt{Q_{00}Q_{2}} & 2Q_L/\sqrt{Q_{1} Q_2} & -1 + 2Q_L/Q_{2} \\
# \end{array}\right)
# $$
# 
# (NOTE: there is a typo in the afr_noise paper by Ishikawa and co. - their $S_{13}$ entry is wrong.)
# 
# My understanding of the notation here is that $Q_{00}$ is the unloaded Q of the cavity, $Q_L$ is the loaded Q of the cavity, $Q_1$ and $Q_2$ are quality factors parameterizing the coupling ports, and $Q_0$ is the active Q (unloaded).
# 
# In the language of coupling coefficients, $\beta_1 = \sqrt{\frac{Q_{00}}{Q_1}}$ and $\beta_2 = \sqrt{\frac{Q_{00}}{Q_2}}$.
# 
# The relationship between the active Q and the other quality factors is given by:
# 
# \begin{align}
# \frac{1}{Q_0} = \frac{1}{Q_L} - 2\sqrt{\frac{G}{Q_1 Q_2}}.
# \end{align}
# 
# Physically, the above equation tells us that a loaded cavity quality factor will be further modified by the introduction of gain, which will act as a negative resistance. When 
# 
# $$
# \sqrt{G} = \frac{\sqrt{Q_1 Q_2}}{2 Q_L}
# $$
# 
# then the active quality factor goes to infinity, and the circuit becomes an oscillator. The equation above is the same as the condition that $S_{23}\sqrt{G} = 1$.
# 
# Now that we've established our notation, we want to know what the output power would look like. If we take the output from port 1 ($b_1$) as the voltage we will be listening to, then $b_1$ has the form:
# 
# $$
# b_1(t)= S_{21} n_0 + S_{22} n_b + S_{23} \sqrt{G} \big(b_1(t- t_0) + n_a\big)
# $$
# 
# Note that we $b_1$ is evaluated at two different times in this equation - once at the current time $t$ but also at $t-t_0$, where $t_0 = L/c$ is the time it takes for a wave at port 1 to traverse the circuit's length $L$.
# 
# The time-averaged power we expect then is:
# 
# $$
# <|b_1(t)|^2> + |S_{23}|^2 G <|b_1(t-t_0)|^2> - 2 S_{23} \sqrt{G} < b_1^*(t)b_1(t-t_0)> = |S_{21}|^2 N_0 + |S_{22}|^2 N_b + |S_{23}|^2 G N_a.
# $$
# 
# where we assumed that there is no correlation between the various noise sources, e.g. $<n_0 n_b> = 0$.
# 
# Let us assume a steady state solution such that $<|b(t)|^2> = <|b(t-t_0)|^2>$. The autocorrelation of the two $b_1(t)$ terms is given by (NOTE: ask Gray again about how this was gotten):
# 
# $$
# <b_1^*(t)b_1(t-t_0)> = <|b_1(t)|^2> e^{-\omega t_0/Q}
# $$
# 
# I drop the subscript $1$ on $b(t)$ for simplicity and denote it by $b_{noise}$. We can rewrite the output power (CHECK: hopefully my transform to frequency space is not sketchy) as
# 
# $$
# <|b_{noise}(\omega)|^2> = \frac{|S_{21}|^2 N_0 + |S_{22}|^2 N_b + |S_{23}|^2 G N_a}{1 + |S_{23}|^2 G - 2S_{23}\sqrt{G}e^{-\omega t_0/Q}}.
# $$
# 
# Finally, we can parametrize any additional phase shift in the circuit by rewriting $\sqrt{G} \rightarrow \sqrt{G}e^{i\theta}$, so
# 
# $$
# <|b_{noise}(\omega)|^2> = \frac{|S_{21}|^2 N_0 + |S_{22}|^2 N_b + |S_{23}|^2 G N_a}{1 + |S_{23}|^2 G - 2S_{23}\sqrt{G}e^{-\omega t_0/Q - i\theta}}.
# $$
# 
# Note that we've derived the output noise power in the case of noise signal, but the output power when a signal is injected into the system (ie $a_0 = \sqrt{\beta_0} p$) would only be modified to be:
# 
# $$
# <|b_{signal}(\omega)|^2> =\frac{|S_{21}|^2 \beta_0 P}{1 + |S_{23}|^2 G - 2S_{23}\sqrt{G}e^{-\omega t_0/Q - i\theta}}
# $$
# 
# so the SNR would be:
# 
# $$
# SNR = \frac{<|b_{signal}(\omega)|^2>}{<|b_{noise}(\omega)|^2>} = \frac{|S_{21}|^2 \beta_0 P}{|S_{21}|^2 N_0 + |S_{22}|^2 N_b + |S_{23}|^2 G N_a}
# $$
# 
# ... this doesn't make any sense. Not sure what I did wrong here.
# 
# In any case, for typical experimental parameters, we can plot the noise vs Q for different delay times, which correspond to our measurement configurations with and without the delay line in. See below.

### Simulation Plots <a id='simulations'></a>

####### Experimental Values:

# In[139]:

Q_cav = 2000.
Q_1 = Q_cav
Q_2 = 15000
Q_L = 1 / (1/Q_cav + 1/Q_1 + 1/Q_2)
omega_0 = 2 * np.pi * 2.256e9
t_0 = 1 / 1.e9 # no phase delay, with phase delay t_0 = 1 / 1.e6
theta = 0 #set additional phase shift equal to 0

N_0 = 300 #kelvin
N_a = 300 #our amplifiers have a NF of 3 dB
N_b = 300 #not sure how to measure the backwards noise?


# In[127]:

S = [[-1 + 2 * Q_L/Q_cav , 2 * Q_L/np.sqrt(Q_cav * Q_1) , 2 * Q_L/np.sqrt(Q_cav * Q_2)],
    [2 * Q_L/np.sqrt(Q_cav * Q_1), -1 + 2 * Q_L/Q_1, 2 * Q_L/np.sqrt(Q_1 * Q_2)],
    [2 * Q_L/np.sqrt(Q_cav * Q_2), 2 * Q_L/np.sqrt(Q_1 * Q_2), -1 + 2 * Q_L/Q_2]]

def active_Q(G):
    return 1 / (1/Q_L - 2 * np.sqrt(G) / np.sqrt(Q_1 * Q_2))

def output_power(G, Q, t):
    numer = S[1][0]**2 * N_0 + S[1][1]**2 * N_b + S[1][2]**2 * G * N_a
    denom = 1 + S[1][2]**2 * G - 2 * S[1][2] * np.sqrt(G) * np.exp( - omega_0 * t / Q) * np.cos(theta)
    try:
        return numer / denom
    except Exception as e:
        raise Exception(str(e))


# In[138]:

gains = np.linspace(0.01, 7, 50)
q_s = [active_Q(g) for g in gains]
t = [1/1.e9, 1/1.e6]
powers_nodelay = [output_power(g, q, t[0]) for g, q in zip(gains, q_s)]
powers_delay = [output_power(g, q, t[1]) for g, q in zip(gains, q_s)]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
fig.set_size_inches(17.5,9)

ax1.plot(q_s, powers_nodelay, 'ko', marker='$\circ$')
ax1.set_xlabel('Q')
ax1.set_ylabel('Noise (Kelvin)')
ax1.set_title('Noise vs Q for t = %.1e' % t[0])


ax2.plot(S[1][2]**2 * gains, powers_nodelay, 'ko', marker='$\circ$')
ax2.set_xlabel('Effective Gain $|S_{23}|^2 G$')
ax2.set_ylabel('Noise (Kelvin)')
ax2.set_title('Noise vs Voltage for t = %.1e' % t[0])

ax3.plot(q_s, powers_delay, 'ko', marker='$\circ$')
ax3.set_xlabel('Q')
ax3.set_ylabel('Noise (Kelvin)')
ax3.set_title('Noise vs Q for t = %.1e' % t[1])


ax4.plot(S[1][2]**2 * gains, powers_delay, 'ko', marker='$\circ$')
ax4.set_xlabel('Effective Gain $|S_{23}|^2 G$')
ax4.set_ylabel('Noise (Kelvin)')
ax4.set_title('Noise vs Voltage for t = %.1e' % t[1]);
fig.savefig('theoretical_noise_behavior.png')


### Measurements <a id='measurements'></a>

# Our actual setup used a delay line (from Teledyne) which added a delay of $~5$ $\mu$seconds.
# 
# We had a variable attenuator as part of the gain scheme, which let us adjsut the total gain and thereby the active Q. There was also a variable phase shifter which we adjusted to find the maximum Q at any given gain setting.
# 
# The procedure was as follows:
# 
# 1. Send in power from the network analyzer to the circuit.
# 
# 2. Adjust the power to the variable phase shifter until the measured Q was maximized.
# 
# 3. Record the Q and cavity resonance.
# 
# 4. Turn off power from the network analyzer by toggling two switches.
# 
# 5. Measure the noise power spectral density of the circuit as displayed on the network analyzer at the cavity resonance.
# 
# 6. Send in a signal (typicaly -40 dBm) into the circuit at the cavity resonance. Record the power spectral density with the signal on.
# 
# 7. Obtain the SNR by subtracting the linear power spectral density measured when the signal was on, vs when it was off.
# 
# 8. Adjust the power to the variable attenuator and repeat steps 1-7.
# 
# The results of our measurements (MEAS6 was without the phase delay, MEAS7 with the phase delay), are shown below. To execute this you will need to change the pathname to point to wherever you have saved MEAS6 and MEAS7.txt

# In[143]:

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharey=True)
fig.set_size_inches(12.5,7.5)
data = np.genfromtxt('/Users/ana/admxactiveresonator/measurements/MEAS7.txt')
Q_7 = data[:, 3]
N = data[:,4]
S = data[:, 5]
Nl_7 = [10**((n+104)/10.) for n in N]
Sl_7 = [10**((s+104)/10.) for s in S]
SNR_7 = [s/n for s, n in zip(Sl_7, Nl_7)]
#ax1.plot(Q, SNR,'bo', label='snr')
ax1.plot(Q_7, Sl_7,'ro', label='signal')
ax1.plot(Q_7, Nl_7,'go', label='noise')
ax1.set_ylim([0, 50])
ax1.legend()
ax1.set_title('MEAS7 - delay line')
ax3.plot(Q_7, SNR_7,'bo', label='snr')
#ax3.set_ylim([0, 300])
ax3.legend()
ax3.set_title('SNR - delay line')
#ax4.plot(Q, Sl,'go', label='signal/phase delay')
#ax4.set_ylim([0, 300])
#ax4.legend()
#ax4.set_title('Signal')
# mpld3.display()
data = np.genfromtxt('/Users/ana/admxactiveresonator/measurements/MEAS6.txt')
Q_6 = data[:, 3]
N = data[:,4]
S = data[:, 5]
Nl_6 = [10**((n+104)/10.) for n in N]
Sl_6 = [10**((s+104)/10.) for s in S]
SNR_6 = [s/n for s, n in zip(Sl_6, Nl_6)]
#ax2.plot(Q, SNR,'bo', label='snr')
ax2.plot(Q_6, Sl_6,'ro', label='signal')
ax2.plot(Q_6, Nl_6,'go', label='noise')
ax2.legend()
ax2.set_title('MEAS6 - no delay line')
#ax3.plot(Q, Nl,'bo', label='noise/no phase delay')
#ax3.set_ylim([0, 300])
#ax3.legend()
#ax3.set_title('Noise')
ax4.plot(Q_6, SNR_6,'bo', label='snr')
#ax4.set_ylim([0, 300])
ax4.legend()
ax4.set_title('SNR - no delay line')
fig.savefig('summary_plots.png')
mpld3.display()
#fig.savefig('summary_plots.png')


### Comparison <a id='comparison'></a>

# Let us plot the simulated noise and measured noise vs Q. We'll probably have to scale the simulation to get it to fit with the measurements.

# In[147]:

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
fig.set_size_inches(17.5,9)
scale = 1 / 1.e8
ax1.plot(q_s, scale * powers_nodelay, 'ko', marker='$\circ$', label='simulation')
ax1.plot(Q_6, Nl_6,'go', label='noise')
ax1.legend()
ax1.set_title('Noise vs Q, no delay')


# In[ ]:



