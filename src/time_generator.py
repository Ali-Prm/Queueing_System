
import numpy as np 
import time 
import heapq

# Arrival time and service time are generated from exponential random varites.  
# Arrival and service mean time.
mean_arrival = 5 
mean_service = 4 
# Intial value for LINEAR CONGRUENTIAL GENERATORS random-number generator.
initial_sequence_arrival = 1697712905  #(seed)
initial_sequence_service = 247165065   #(seed)
multiplier = 16807
modulus = 2147483648



class RandomTimeGenerator():
    """
    Exponential random varites generator based on the Inverse Transform method.
    Random numbers are generated using the LINEAR CONGRUENTIAL GENERATORS method.
    """
    def __init__(self,
                initial_sequence, mean, modulus, multiplier):
        self.sequence = initial_sequence
        self.random_number = None
        self.mean = mean
        self.modulus = modulus
        self.multiplier = multiplier
        
    def sequence_next_value(self):
        next_seq = (self.multiplier*self.sequence) % self.modulus
        self.sequence = next_seq
        return next_seq
    
    def compute_random_number(self):
        self.random_number = self.sequence / self.modulus
        
    def compute_exponential_varites(self):
        exponential_varites = -self.mean * np.log(self.random_number)
        return exponential_varites

    def __str__(self):
        return "This is the stochastic exponential time generator."



def time_generator_helper(random_time_obj):
    """
    Helper function for generating sequence of random varites.
    """
    random_time_obj.compute_random_number()
    output = random_time_obj.compute_exponential_varites()
    random_time_obj.sequence_next_value()
    return output 


if __name__ == '__main__':
    interarrival_obj = RandomTimeGenerator(initial_sequence=initial_sequence_arrival,
                                        mean=mean_arrival, modulus=modulus, multiplier=multiplier)

    service_obj = RandomTimeGenerator(initial_sequence=initial_sequence_service,
                                        mean=mean_service, modulus=modulus, multiplier=multiplier)
    for i in range(10):
        value = time_generator_helper(interarrival_obj)
        print(value)
