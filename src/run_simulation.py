import numpy as np 
import time 
import heapq

def run_simulation(queue, sys_type):
    """
    Helper function for ruuning the queueing system. (FCFS and SPT)
    """    
    start = time.time()
    # Initialize the queue object 
    queue.initialize()
    # Run the simulation until the stopping crietria is met. 
    while queue.sim_time <= queue.stopping_time :
        
        queue.timing()
        queue.update_time_avg_stats()
        
        if queue.next_event_type == 'arrival':
            queue.arrival()
            
        elif queue.next_event_type == 'departure' :
            queue.departure()
            
        elif queue.next_event_type == 'termination' :
            queue.timing()
            queue.update_time_avg_stats()
            break
        
    if queue.service_time_type == 'stochastic':
        desc = 'M'
    else :
        desc = 'D'
    
    end = time.time()   
    running_time = end-start
    
    if queue.stopping_criteria == 'time':
        text = f'Elapsed Time:{queue.stopping_time} Minutes'
    else :
        text = f'No.of Served Entities:{queue.num_custs_delayed}'
    
    print (f"Info:   M/{desc}/1 | {sys_type} | {text}")
    print('----------------------------')
    queue.timing()
    queue.update_time_avg_stats()
    queue.report()
    print('----------------------------') 
    print(f'Running Time : {running_time}')
    