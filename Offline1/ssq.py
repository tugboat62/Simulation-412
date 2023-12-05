import math
from lcgrand import LCG

class QueueingSystem:
    def __init__(self, arrival_mean, service_mean, total_delays):
        self.arrival_mean = arrival_mean
        self.service_mean = service_mean
        self.total_delays = total_delays
        self.clock = 0.0
        self.next_arrival_time = self.generate_interarrival()
        self.next_departure_time = math.inf
        self.queue = []
        self.num_delays = 0
        self.total_delay_time = 0.0
        self.server_busy = False

    def generate_interarrival(self):
        lcg = LCG()
        return -self.arrival_mean * math.log(lcg.generate())

    def generate_service(self):
        lcg = LCG()
        return -self.service_mean * math.log(lcg.generate())

    def simulate(self):
        with open("event_orders.txt", "w") as events_file:
            while self.num_delays < self.total_delays:
                if self.next_arrival_time < self.next_departure_time:
                    self.handle_arrival(events_file)
                else:
                    self.handle_departure(events_file)

            avg_delay_in_queue = self.total_delay_time / self.total_delays
            avg_customers_in_queue = sum(len(q) for q in self.queue) / self.clock
            avg_server_utilization = (self.clock - self.next_departure_time) / self.clock

            with open("results.txt", "w") as results_file:
                results_file.write(f"Average Delay in Queue: {avg_delay_in_queue:.4f}\n")
                results_file.write(f"Average Number of Customers in Queue: {avg_customers_in_queue:.4f}\n")
                results_file.write(f"Average Server Utilization: {avg_server_utilization:.4f}\n")

    def handle_arrival(self, events_file):
        self.clock = self.next_arrival_time
        self.next_arrival_time += self.generate_interarrival()
        if self.server_busy:
            self.queue.append(self.clock)
            events_file.write(f"{self.clock:.4f} Arrival - Customer queued\n")
        else:
            self.server_busy = True
            service_time = self.generate_service()
            self.next_departure_time = self.clock + service_time
            events_file.write(f"{self.clock:.4f} Arrival - Customer starts service\n")

    def handle_departure(self, events_file):
        self.clock = self.next_departure_time
        if len(self.queue) == 0:
            self.server_busy = False
            self.next_departure_time = math.inf
            events_file.write(f"{self.clock:.4f} Departure - Server idle\n")
        else:
            customer_delayed = self.queue.pop(0)
            self.num_delays += 1
            self.total_delay_time += self.clock - customer_delayed
            service_time = self.generate_service()
            self.next_departure_time = self.clock + service_time
            events_file.write(f"{self.clock:.4f} Departure - Customer leaves queue and starts service\n")

if __name__ == "__main__":
    with open("input.txt", "r") as input_file:
        A, S, N = map(float, input_file.readline().split())

    queue_system = QueueingSystem(A, S, N)
    queue_system.simulate()
