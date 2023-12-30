import math
from lcgrand import lcgrand

Q_LIMIT = 1000  # Limit on queue length.
BUSY = 1       # Mnemonics for server's being busy
IDLE = 0       # and idle.

next_event_type = 0
num_custs_delayed = 0
num_delays_required = 0
num_events = 0
num_in_q = 0
server_status = []
num_servers = 0
event_count = 1
cust_arr = 0
cust_dep = 0
area_num_in_q = 0.0
area_server_status = 0.0
mean_interarrival = 0.0
mean_service = 0.0
sim_time = 0.0
time_arrival = [0.0] * (Q_LIMIT + 1)
time_last_event = 0.0
time_next_event = [0.0] * 3
total_of_delays = 0.0
event_orders_file = None
results_file = None
event_orders_file = open("event_orders.txt", "w")
results_file = open("results.txt", "w")
cust_served = 0

num_events = 2
infile = open('in.txt', "r")

def initialize():
    global server_status, time_next_event

    server_status = [0] * num_servers
    time_next_event[1] = sim_time + expon(mean_interarrival)
    time_next_event[2] = 1.0e+30


def timing():
    global next_event_type, num_events, time_next_event, sim_time

    min_time_next_event = 1.0e+29
    next_event_type = 0

    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    if next_event_type == 0:
        results_file.write(f"\nEvent list empty at time {sim_time}")
        exit(1)

    sim_time = min_time_next_event


def arrive():
    global sim_time, server_status, num_in_q, num_custs_delayed, total_of_delays, time_next_event

    global event_count, cust_arr, cust_served

    cust_arr += 1
    event_orders_file.write(f"{event_count}. Next event: Customer {cust_arr} Arrival\n")
    event_count += 1
    time_next_event[1] = sim_time + expon(mean_interarrival)

    done = False
    for i in range(num_servers):
        if server_status[i] != IDLE:
            if num_in_q > Q_LIMIT:
                results_file.write(f"\nOverflow of the array time_arrival at time {sim_time}")
                exit(2)
            time_arrival[num_in_q] = sim_time
        else:
            cust_served += 1
            delay = 0.0
            total_of_delays += delay
            num_custs_delayed += 1
            event_orders_file.write(f"\n---------No. of customers delayed: {num_custs_delayed}---------\n\n")
            server_status[i] = cust_served
            time_next_event[2] = sim_time + expon(mean_service)
            done = True
            return cust_served
    if not done: num_in_q += 1
    return 0


def depart():
    global sim_time, num_in_q, num_custs_delayed, total_of_delays, time_next_event

    global event_count, cust_dep

    cust_dep += 1
    event_orders_file.write(f"{event_count}. Next event: Customer {cust_dep} Departure\n")
    event_count += 1
    m = server_status[0]
    idx = 0
    for i in range(1, num_servers):
        if server_status[i] < m:
            m = server_status[i]
            idx = i
    
    if num_in_q == 0:
        server_status[idx] = IDLE
        time_next_event[2] = 1.0e+30
    else:
        num_in_q -= 1
        delay = sim_time - time_arrival[1]
        total_of_delays += delay
        num_custs_delayed += 1
        event_orders_file.write(f"\n---------No. of customers delayed: {num_custs_delayed}---------\n\n")
        time_next_event[2] = sim_time + expon(mean_service)

        for i in range(1, num_in_q + 1):
            time_arrival[i] = time_arrival[i + 1]


def report():
    global total_of_delays, num_custs_delayed, area_num_in_q, sim_time, area_server_status, results_file

    results_file.write(f"Average delay in queue: {total_of_delays / num_custs_delayed:.3f} minutes\n")
    results_file.write(f"Average number in queue: {area_num_in_q / sim_time:.3f}\n")
    results_file.write(f"Server utilization: {area_server_status / sim_time:.3f}\n")
    results_file.write(f"Time simulation ended: {sim_time:.3f} minutes")


def update_time_avg_stats():
    global num_in_q, area_num_in_q, server_status, area_server_status, sim_time, time_last_event

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    area_num_in_q += num_in_q * time_since_last_event
    for i in range(num_servers):
        if server_status[i] != IDLE:
            area_server_status += server_status[i] * time_since_last_event


def expon(mean):
    return -mean * math.log(lcgrand(1))


def main():
    global num_delays_required, num_events, num_custs_delayed, total_of_delays, area_num_in_q, server_status, area_server_status, event_orders_file, results_file

    global mean_interarrival, mean_service
    global next_event_type, time_next_event, sim_time, num_custs_delayed, cust_arr, cust_dep, event_count, num_servers

    num_servers, mean_interarrival, mean_service, num_delays_required = map(float, infile.readline().split())
    num_servers = int(num_servers)
    results_file.write("----Single-Server Queueing System----\n\n")
    results_file.write(f"Mean interarrival time: {mean_interarrival:.3f} minutes\n")
    results_file.write(f"Mean service time: {mean_service:.3f} minutes\n")
    results_file.write(f"Number of customers: {int(num_delays_required)}\n\n")

    initialize()

    while num_custs_delayed < num_delays_required:
        timing()
        update_time_avg_stats()
        cust_no = 0
        if next_event_type == 1:
            arrive()
        elif next_event_type == 2:
            depart()

    report()
    infile.close()
    event_orders_file.close()
    results_file.close()


if __name__ == "__main__":
    main()
