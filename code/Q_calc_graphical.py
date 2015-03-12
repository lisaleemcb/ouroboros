import matplotlib.pylab as plt
import numpy as np

#initialization stuff
file = "../data/S12.s2p"
data = np.genfromtxt(file,skip_header=12)

freq = data[:,0]
voltage = data[:,3]

#data processing stuff
max_power = np.max(voltage)
max_power_index = np.argmax(voltage)

max_freq = freq[max_power_index]

three_dB = max_power - 3.0
vals_BELOW = np.where(voltage > three_dB)
vals_ABOVE = np.where((voltage < three_dB) & (freq > max_freq))

three_dB_freq_BELOW = freq[vals_BELOW[0][0]]
three_dB_freq_ABOVE = freq[vals_ABOVE[0][0]]
delta_freq = three_dB_freq_ABOVE - three_dB_freq_BELOW

Q_L = max_freq / delta_freq
print(Q_L)


#plotting stuff
plt.xlabel(r'Frequency (GHz)')
plt.ylabel(r'Power (dBm/Hz)')
plt.annotate(r' $ f_{L} $ ',xy=(freq[max_power_index], max_power), xytext=(freq[max_power_index], max_power))
plt.axhline(y= three_dB,ls='dashed')
#plt.axvline(x= three_dB_freq_BELOW,ls='dashed')
#plt.axvline(x= three_dB_freq_ABOVE,ls='dashed')
plt.annotate("",
            xy=(three_dB_freq_BELOW, three_dB), xycoords='data',
            xytext=(three_dB_freq_ABOVE, three_dB), textcoords='data',
            arrowprops=dict(arrowstyle="<->",
                            connectionstyle="arc3"),)
#plt.annotate(
#            r'$ \Delta $ ', xy=(max_freq-20, three_dB-20), xycoords='data',
#            xytext=(three_dB_freq_BELOW, three_dB - .1), textcoords='offset points')

plt.text(three_dB_freq_BELOW, three_dB - 2, r'$ \Delta f $')
plt.text(three_dB_freq_ABOVE + 2e6, three_dB - 5, r'$ Q = 841.225225225 $')

plt.plot(freq,voltage)
plt.show()
