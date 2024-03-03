import numpy as np
import matplotlib.pyplot as plt

def secretary_problem(n, s, num_simulations=1000):
    success_counts = np.zeros(n)
    
    for _ in range(num_simulations):
        for m in range(n):
            rankings = np.random.permutation(n) + 1  # Simulating unique ranks from 1 to n
            if m == 0:
                if rankings[0] <= s: success_counts[m] += 1
                continue
            # Select the first m candidates as the sample
            sample = rankings[ :m]

            # Determine the standard based on the sample
            standard = np.min(sample)
            selected = False
            for i in range(m, n):
                if rankings[i] < standard:
                    if rankings[i] <= s: success_counts[m] += 1
                    selected = True
                    break
                
            if not selected: 
                if rankings[n-1] <= s: success_counts[m] += 1

    success_rate = success_counts * 100 / num_simulations
    return success_rate

def plot_success_rate(n, s):
    m_values = np.arange(1, n+1)  # Skip sample size of 0
    success_rate = secretary_problem(n, s)

    plt.plot(m_values, success_rate, label=f's={s}')
    plt.ylim(0, 100)
    plt.xlabel('Sample Size (m)')
    plt.ylabel('Success Rate')
    plt.title(f'Success Rate vs. Sample Size for n={n}')
    plt.legend()
    plt.show()

# Plot for n=100 and different success criteria s
n = 100
success_criteria_values = [1, 3, 5, 10]

for s in success_criteria_values:
    plot_success_rate(n, s)
