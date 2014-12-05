import numpy as np
import matplotlib.pyplot as plt

G = np.linspace(0,5)
T_1 = 1/G
T_2 = 1/(G**2)

plt.plot(G,T_1, label=r'$\frac{1}{G}$')
plt.plot(G,T_2, label=r'$\frac{1}{G^{2}}$')

plt.yscale('log')
plt.xlim((0,5))
plt.ylim((0,100))


plt.legend(loc='upper left', borderaxespad=1)
plt.show()
