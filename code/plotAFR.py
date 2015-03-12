from scipy import *
from matplotlib import *
from matplotlib.pyplot import *

k_B = 1.381e-23 # Boltzmann constant (J/K)

fileMEAS6 = "MEAS6.txt"
fileMEAS7 = "MEAS7.txt"
fileMEAS6cutsort = "MEAS6cutsort.txt"
fileMEAS7cutsort = "MEAS7cutsort.txt"

MEAS6 = genfromtxt(fileMEAS6)
MEAS7 = genfromtxt(fileMEAS7)
MEAS6cutsort = genfromtxt(fileMEAS6cutsort)
MEAS7cutsort = genfromtxt(fileMEAS7cutsort)

#variables
voltagePS6 = MEAS6[:,0]
voltagePS7 = MEAS7[:,0]
voltagePS6cutsort = MEAS6cutsort[:,0]
voltagePS7cutsort = MEAS7cutsort[:,0]

voltagePhase6 = MEAS6[:,1]
voltagePhase7 = MEAS7[:,1]
voltagePhase6cutsort = MEAS6cutsort[:,1]
voltagePhase7cutsort = MEAS7cutsort[:,1]


freqVNA6 = MEAS6[:,2]
freqVNA7 = MEAS7[:,2]
freqVNA6cutsort = MEAS6cutsort[:,2]
freqVNA7cutsort = MEAS7cutsort[:,2]

Q6 = MEAS6[:,3]
Q7 = MEAS7[:,3]
Q6cutsort = MEAS6cutsort[:,3]
Q7cutsort = MEAS7cutsort[:,3]

noise6 = MEAS6[:,4]
noise7 = MEAS7[:,4]
noise6cutsort = MEAS6cutsort[:,4]
noise7cutsort = MEAS7cutsort[:,4]

signal6 = MEAS6[:,5]
signal7 = MEAS7[:,5]
signal6cutsort = MEAS6cutsort[:,5]
signal7cutsort = MEAS7cutsort[:,5]

logSNR6 = signal6 - noise6
logSNR7 = signal7 - noise7
logSNR6cutsort = signal6cutsort - noise6cutsort
logSNR7cutsort = signal7cutsort - noise7cutsort

linSNR6 = 10.0**(logSNR6/10.0)
linSNR7 = 10.0**(logSNR7/10.0)
linSNR6cutsort = 10.0**(logSNR6cutsort/10.0)
linSNR7cutsort = 10.0**(logSNR7cutsort/10.0)

linNoise6cutsort = 10.0**((noise6cutsort)/10.0)
linNoise7cutsort = 10.0**((noise7cutsort)/10.0)
linSignal7 = 10.0**((signal7)/10.0)
linSignal6cutsort = 10.0**((signal6cutsort)/10.0)
linSignal7cutsort = 10.0**((signal7cutsort)/10.0)
linNoiseTemp6cutsort = linNoise6cutsort / (1000 * k_B)
linNoiseTemp7cutsort = linNoise7cutsort / (1000 * k_B)


#change to the desired variable; hence, desvar
desvarX = 'Q'
desvarY = 'linNoiseTemp'
desvarX6 = desvarX + '6cutsort'
desvarX7 = desvarX + '7cutsort'
desvarY6 = desvarY + '6cutsort'
desvarY7 = desvarY + '7cutsort'

X6 = eval(desvarX6)
Y6 = eval(desvarY6)

X7 = eval(desvarX7)
Y7 = eval(desvarY7)

coefficients1_MEAS6 = polyfit(X6, Y6, 1)
coefficients1_MEAS7 = polyfit(X7, Y7, 1)

coefficients2_MEAS6 = polyfit(X6, Y6, 2)
coefficients2_MEAS7 = polyfit(X7, Y7, 2)

poly1_MEAS6 = poly1d(coefficients1_MEAS6) # construct the polynomial
poly1_MEAS7 = poly1d(coefficients1_MEAS7) # construct the polynomial

poly2_MEAS6 = poly1d(coefficients2_MEAS6) # construct the polynomial
poly2_MEAS7 = poly1d(coefficients2_MEAS7) # construct the polynomial

#print(coefficients1)
#print(coefficients2)

fig, ax1 = subplots()
ax1.plot(X6, Y6, 'o', label='MEAS 6')
ax1.plot(X7, Y7, 'o', label='MEAS 7')

#plot(X6, poly1_MEAS6(X6), label='linear fit')
#plot(X7, poly1_MEAS7(X7), label='linear fit')

#plot(X6, poly2_MEAS6(X6), label='quadratic fit')
#plot(X7, poly2_MEAS7(X7), label='quadratic fit')

ax2 = ax1.twiny()
#ax2.plot(Q6cutsort,Y6,'o')
#ax2.set_xlim(0,6000)
ax1.set_xlabel('Gain Voltage (V)')
ax2.set_xlabel('corresponding Q-factor (roughly)')
ax1.set_ylabel('Noise (mW)')
#legend()
show()
