import numpy as np
import matplotlib.pyplot as plt

# Given probability distribution pi
def pi(i):
    return (0.2126) * (0.5893) ** (i - 1)

probs = [1 - (pi(1) + pi(2) + pi(3)), pi(1), pi(2), pi(3)]

# Function to simulate neutron production for one generation
def simulate_generation():
    return np.random.choice([0, 1, 2, 3], p=probs)

# Function to simulate chain reaction for multiple generations
def simulate_chain_reaction(num_generations, num_simulations):
    results = np.zeros((num_simulations, num_generations), dtype=int)    

    for j in range(num_simulations):
        neutrons = 1
        for i in range(num_generations):
            new_neutrons = sum(simulate_generation() for _ in range(neutrons))
            results[j, i] = new_neutrons
            neutrons = new_neutrons

    return results

# Function to calculate probabilities for each number of neutrons
def calculate_probabilities(results):
    num_simulations, num_generations = results.shape
    probabilities = np.zeros((num_generations, 5))

    for j in range(num_generations):
        unique, counts = np.unique(results[:, j], return_counts=True)
        max_index = min(len(unique), 4)  # Ensure the index doesn't go out of bounds
        probabilities[j, unique[:max_index+1]] = counts[:max_index+1] / num_simulations

    return probabilities

# Simulate chain reaction for 10 generations, 10,000 times
num_generations = 10
num_simulations = 10000
simulation_results = simulate_chain_reaction(num_generations, num_simulations)

# Calculate probabilities for each number of neutrons
probabilities = calculate_probabilities(simulation_results)

file_path = "fission_output.txt"
with open(file_path, "w") as file:
    # Write content to the file
    for i in range(num_generations):
        file.write(f"Generation-{i + 1}:\n") 
        for j in range(5):
            file.write(f"p[{j}] = {probabilities[i][j]:.4f}\n")
        file.write("\n")
