import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import norm



a = {'weekly': {-3: 32, -2: 18, -1: 13, 0: 1, 1: 11, 2: 2, 3: 4}, 'monthly': {-3: 3, -2: 3, -1: 12, 0: 2, 1: 21, 2: 24, 3: 16}, 'as_usual': {-3: 1, -2: 5, -1: 0, 0: 8, 1: 15, 2: 29, 3: 23}}
b = a.values()

c = [list(x.values()) for x in b]

c[0] = c[0][::-1]

arr = np.array(c)

s = arr.sum(axis = 0)
ds = [sum(s[:i+1]) for i in range(len(s))]
ds/=ds[-1]
print(ds)
ms = arr.mean(axis = 0)

m = ms/ms.sum()
plt.bar(np.linspace(-3,3,7),m)
plt.xlabel("Motivation")
plt.ylabel("Probability of expression")
plt.title("Approximated Trend Motivation Distribution in the Mowing Scenario (Mass function)")
plt.show()

plt.bar(np.linspace(-3,3,7),ds)
plt.xlabel("Motivation")
plt.ylabel("Probability of expression")
plt.title("Approximated Trend Motivation Distribution in the Mowing Scenario")
plt.show()


