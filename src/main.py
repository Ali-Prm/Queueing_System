import numpy as np 
import time 
import heapq

from fcfs import SingleServerQueuing_FCFS
from spt import SingleServerQueuing_SPT
from time_generator import RandomTimeGenerator
from time_generator import time_generator_helper
from run_simulation import run_simulation



# Arrival time and service time are generated from exponential random varites.  
# Arrival and service mean time.
mean_arrival = 5 
mean_service = 4 
# Intial value for LINEAR CONGRUENTIAL GENERATORS random-number generator.
initial_sequence_arrival = 1697712905  #(seed)
initial_sequence_service = 247165065   #(seed)
multiplier = 16807
modulus = 2147483648


# Stochastic arrival time generator 
interarrival_obj = RandomTimeGenerator(initial_sequence=initial_sequence_arrival,
                                        mean=mean_arrival, modulus=modulus, multiplier=multiplier)
# Stochastic service time generator 
service_obj = RandomTimeGenerator(initial_sequence=initial_sequence_service,
                                        mean=mean_service, modulus=modulus, multiplier=multiplier)

# Initializing FCFS M/M/1 with 1000 entities.
queue_fcfs = SingleServerQueuing_FCFS(
    stopping_criteria='custs_num',num_delayed_required =10000,
    stopping_time=np.inf, service_time_type='stochastic', mean_service_time=4,
    interarrival_obj=interarrival_obj, service_obj=service_obj)
# Running the simulation for FCFS M/M/1 with 1000 entities.
run_simulation(queue=queue_fcfs, sys_type='FCFS')

print('')

# Stochastic arrival time generator 
interarrival_obj = RandomTimeGenerator(initial_sequence=initial_sequence_arrival,
                                        mean=mean_arrival, modulus=modulus, multiplier=multiplier)
# Stochastic service time generator 
service_obj = RandomTimeGenerator(initial_sequence=initial_sequence_service,
                                        mean=mean_service, modulus=modulus, multiplier=multiplier)

# Initializing SPT M/M/1 with 1000 entities.
queue_spt = SingleServerQueuing_SPT(
    stopping_criteria='custs_num',num_delayed_required =10000,
    stopping_time=np.inf, service_time_type='stochastic', mean_service_time=4,
    interarrival_obj=interarrival_obj, service_obj=service_obj)
# Running the simulation for FCFS M/M/1 with 1000 entities.
run_simulation(queue=queue_spt, sys_type='SPT')