import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# parameters
mu = 0
sigma = 1
num_samples = 100_000
k = np.arange(-5, 6)
print(k)
# discrete Gaussian via CDF differences
pmf = norm.cdf(k + 0.5, mu, sigma) - norm.cdf(k - 0.5, mu, sigma)
pmf /= pmf.sum()

# sample
samples = np.random.choice(k, size=num_samples, p=pmf)

# plot histogramFalse
plt.hist(samples, bins=len(k), density=True)
plt.xlabel("k")
plt.ylabel("Probability")
plt.title("Discrete Gaussian (CDF Difference Sampling)")
plt.show()