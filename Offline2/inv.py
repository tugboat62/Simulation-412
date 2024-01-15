import math
from lcgrand import *

# Initial inventory level, number of months, number of policies
I, N, P = 0, 0, 0

# Number of demand size and Mean inter demand time in months 
D, beta_D = 0, 0

# Setup Cost, per-unit Incremental Cost, Holding Cost & Shortage Cost
K, i, h, pi = 0, 0, 0, 0

# Minlag and Maxlag periods in months
m, M = 0, 0

# cumulative probabilities of the sequential demand sizes
cum_prob = []

# policies
s, S = 0, 0
#Average Ordering, Holding, Shortage and Total Costs for each given policy
avg_ord = 0
avg_hold = 0
avg_short = 0
total_costs = [0] * P

output_file = open("out.txt", "w")
infile = open('in.txt', "r")

# Initialize the next_event_type variable.
next_event_type = 1
# Initialize the simulation clock.
sim_time = 0.0

num_events = 4
time_last_event = 0.0
# Initialize the statistical counters.
total_ordering_cost = 0.0
amount = 0.0
area_holding = 0.0
area_shortage = 0.0
time_next_event = [0] * 5

inv_level = 0

def main():
    global I, N, P, D, beta_D, K, i, h, pi, m, M, cum_prob
    global s, S, avg_ord, avg_hold, avg_short, total_costs
    
    # Read input parameters
    I, N, P = map(int, infile.readline().split())
    D, beta_D = map(float, infile.readline().split())
    D = int(D)
    K, i, h, pi = map(float, infile.readline().split())
    m, M = map(float, infile.readline().split())
    
    prob = list(map(float, infile.readline().split()))
    cum_prob.append(0.0)

    for j in range(D):
        cum_prob.append(prob[j])
        
    output_file.write("------Single-Product Inventory System------\n\n")
    output_file.write(f"Initial inventory level: {I} items\n\n")
    output_file.write(f"Number of demand sizes: {D}\n\n")
    output_file.write(f"Distribution function of demand sizes: {' '.join(map(str, prob))}\n\n")
    output_file.write(f"Mean inter-demand time: {beta_D:.2f} months\n\n")
    output_file.write(f"Delivery lag range: {m:.2f} to {M:.2f} months\n\n")
    output_file.write(f"Length of simulation: {N} months\n\n")
    output_file.write(f"Costs:\nK = {K}\ni = {i}\nh = {h}\npi = {pi}\n\n")
    output_file.write(f"Number of policies: {P}\n\n")
    output_file.write(f"Policies\n")
    output_file.write(f"--------------------------------------------------------------------------------------------------\n")
    output_file.write(f"Policy\t\tAvg_total_cost\t\tAvg_ordering_cost\t\tAvg_holding_cost\t\tAvg_shortage_cost\n")
    output_file.write(f"--------------------------------------------------------------------------------------------------\n\n")

    for j in range(P):
        s, S = map(int, infile.readline().split())
        initialize()
        while True:
            # Determine the next event.
            timing()
            
            # Update time-average statistical accumulators.
            update_time_avg_stats()
            
            # Invoke the appropriate event function.
            if next_event_type == 1:
                order_arrival()
            elif next_event_type == 2:
                demand()
            elif next_event_type == 4:
                evaluate()
            elif next_event_type == 3:
                report()
            
            if next_event_type == 3:
                break
    
    output_file.write(f"--------------------------------------------------------------------------------------------------")
        
    output_file.close()
    infile.close()

def timing():
    global next_event_type, num_events, time_next_event, sim_time

    min_time_next_event = 1.0e+29
    next_event_type = 0

    for j in range(1, num_events + 1):
        if time_next_event[j] < min_time_next_event:
            min_time_next_event = time_next_event[j]
            next_event_type = j

    if next_event_type == 0:
        results_file.write(f"\nEvent list empty at time {sim_time}")
        exit(1)

    sim_time = min_time_next_event


def initialize():
    global inv_level, time_next_event, I, sim_time, time_last_event, total_ordering_cost, area_holding, area_shortage
    # Initialize the state variables.
    inv_level = I
    
    sim_time = 0.0
    time_last_event = 0.0
    
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0

    # Initialize the event list. Since no order is outstanding, the order-arrival event is eliminated from consideration.
    time_next_event[1] = 1.0e+30
    time_next_event[2] = sim_time + expon(beta_D)
    time_next_event[3] = N
    time_next_event[4] = 0.0

def order_arrival():
    global inv_level, time_next_event
    # Increment the inventory level by the amount ordered.
    inv_level += amount
    # Since no order is now outstanding, eliminate the order-arrival event from consideration.
    time_next_event[1] = 1.0e+30

def demand():
    global inv_level, time_next_event
    # Decrement the inventory level by a generated demand size.
    inv_level -= random_integer(cum_prob)
    # Schedule the time of the next demand.
    time_next_event[2] = sim_time + expon(beta_D)

def evaluate():
    global inv_level, time_next_event, amount, total_ordering_cost, s, m, M, S, K, i 

    if inv_level < s:
        # The inventory level is less than s, so place an order for the appropriate amount.
        amount = S - inv_level
        total_ordering_cost += K + i * amount

        # Schedule the arrival of the order.
        time_next_event[1] = sim_time + uniform(m, M)

    # Regardless of the place-order decision, schedule the next inventory evaluation.
    time_next_event[4] = sim_time + 1.0

def report():
    global total_ordering_cost, area_holding, area_shortage, N, h, pi, s, S, out_file

    # Compute and write estimates of desired measures of performance.
    avg_holding_cost = h * area_holding / N
    avg_ordering_cost = total_ordering_cost / N
    avg_shortage_cost = pi * area_shortage / N

    output_file.write(f"({s}, {S}){' ' * 2}{avg_ordering_cost + avg_holding_cost + avg_shortage_cost:15.2f}"
                  f"{' ' * 6}{avg_ordering_cost:15.2f}{' ' * 3}{avg_holding_cost:15.2f}{' ' * 12}{avg_shortage_cost:15.2f}\n\n")


def update_time_avg_stats():
    global sim_time, time_last_event, inv_level, area_shortage, area_holding

    # Compute time since the last event, and update the last-event-time marker.
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    # Determine the status of the inventory level during the previous interval.
    # If the inventory level during the previous interval was negative, update area_shortage.
    # If it was positive, update area_holding. If it was zero, no update is needed.
    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event


def random_integer(prob_distrib):
    j = 1
    u = lcgrand(1)

    # Return a random integer in accordance with the (cumulative) distribution function prob_distrib.
    while u >= prob_distrib[j]:
        j += 1

    return j


def uniform(a, b):
    return a + lcgrand(1) * (b - a)


def expon(mean):
    return -mean * math.log(lcgrand(1))


if __name__ == "__main__":
    main()
