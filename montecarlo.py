import numpy as np
import matplotlib.pyplot as plt

# Monte Carlo setup
n_sims = 1000
days = 252
start_price = 1000
mu = -0.02
sigma = 0.4

simulations = []
for _ in range(n_sims):
    daily_returns = np.random.normal(mu, sigma, days)
    price_series = start_price * np.exp(np.cumsum(daily_returns))
    simulations.append(price_series)

# Convert simulations to NumPy array
simulations = np.array(simulations)  # Now it's a proper 2D NumPy array

# Select 50 simulations
for sim in np.random.choice(simulations.shape[0], size=50, replace=False):  # Select indices
    plt.plot(simulations[sim], alpha=0.3)

plt.title("Monte Carlo Börskrasch Simulering")
plt.xlabel("Dagar")
plt.ylabel("Indexvärde")
plt.show()
