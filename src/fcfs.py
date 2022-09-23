from time_generator import RandomTimeGenerator
from time_generator import time_generator_helper
from run_simulation import run_simulation

import numpy as np
import time
import heapq


class SingleServerQueuing_FCFS():
    
    def __init__(self,
                stopping_criteria,num_delayed_required, stopping_time,
                service_time_type, mean_service_time,
                interarrival_obj, service_obj):

        # Stopping Rule 
        self.stopping_criteria = stopping_criteria
        self.num_delayed_required = num_delayed_required
        self.stopping_time = stopping_time
        
        # Service Time Parameters
        self.service_time_type = service_time_type
        self.mean_service_time = mean_service_time
        
        # Simulation Clock
        self.sim_time = None
        
        # State Variables
        self.server_status = None
        self.num_in_q = None
        self.time_arrival = []
        self.time_last_event = None
        
        # Next Event Type
        self.next_event_type = None

        
        # Statistical Counters
        self.num_custs_delayed = None
        self.num_in_q = None
        self.area_num_in_q = None
        self.area_server_status = None
        self.total_of_delays = None 

        
        # Next Event Time
        self.time_next_event = {'arrival':0.0, 'departure':0.0}
        
        # Number of Entities Waiting More Than Specific Amount of Time In The System ( here: 4.5minutes)
        self.num_custs_wait = None
        self.pct_custs_wait = None
        
        # Interarrival and Service Time Objects 
        self.interarrival_obj = interarrival_obj
        self.service_obj = service_obj
        


    def initialize(self):
        """
        The Initialization Routine: Setting the Initial Value of Attributes.
        """
        # Simulation Clock
        self.sim_time = 0.0
        
        # State Variables
        self.server_status = 'IDLE'
        self.num_in_q = 0
        self.time_last_event = 0.0
        
        # Statistical Counters 
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.num_custs_wait = 0
        self.pct_custs_wait = 0.0
        
        # Next Event Time
        self.time_next_event['arrival'] = self.sim_time + time_generator_helper(self.interarrival_obj) 
        self.time_next_event['departure'] = np.inf
        self.time_next_event['termination'] =  self.stopping_time
        
    
    def timing(self):
        """
        Timing Routine: Determine the next event type and advance the Simulation clock.
        """
        # Setting the initial time of next event at infinite to evaluate the timing routine's correctness.
        self.min_time_next_event = np.inf
        
        # Find the next event time by comapring the time of next departure and arrival event.
        if min(self.time_next_event['arrival'],self.time_next_event['departure']) < self.min_time_next_event :
            
            if min(self.time_next_event['arrival'],self.time_next_event['departure']) < self.time_next_event['termination'] :
                
                if self.time_next_event['arrival'] <=  self.time_next_event['departure'] :
                        self.next_event_type = 'arrival'
                        self.min_time_next_event = self.time_next_event['arrival']
                else :
                        self.next_event_type = 'departure'
                        self.min_time_next_event = self.time_next_event['departure']
                        
            else :
                self.next_event_type = 'termination'
                self.min_time_next_event = self.time_next_event['termination']
                    
            self.sim_time = self.min_time_next_event

        # Return and stop the porgram if next event time is infinity.  
        else: 
            print('time of next event is inf!!') 
            return
            
        
        
    def arrival(self):
        """
        Arrival Routine: Schedule the next arrival event and apply the arrival flowchart.
        """
        # Scheduling The Next Arrival Event
        self.time_next_event['arrival'] = self.sim_time + time_generator_helper(self.interarrival_obj)
        
        # Check the Server Status
        # Server is in the BUSY State
        if self.server_status == 'BUSY':
            self.num_in_q += 1
            self.time_arrival.append(self.sim_time)
            
        # Server is in the IDLE State
        else :
            delay = 0.0
            self.total_of_delays += delay 
            self.num_custs_delayed += 1 
            self.server_status = 'BUSY'

            # Generate The Service Time
            if self.service_time_type == 'stochastic':
                service_times = time_generator_helper(self.service_obj)
            else :
                service_times = self.mean_service_time

            # Schedule The Departure Event.
            self.time_next_event['departure'] = self.sim_time + service_times

            # Check if The Entity is Waiting More Than Specific Amount of Time In The System. ( here: 4.5minutes)
            if service_times + delay >= 4.5 :
                self.num_custs_wait +=1
            else:
                pass
            
            # Check The Stopping Criteria
            if  self.stopping_criteria=='custs_num' and self.num_custs_delayed==self.num_delayed_required :
                self.time_next_event['termination'] = self.time_next_event['departure']
            else :
                pass
                


    def departure(self):
        """
        Departure Routine: The departure flowchart.
        """
        # Check if The Queue is Empty.
        # Empty Queue
        if self.num_in_q == 0 :
            self.server_status = 'IDLE'
            self.time_next_event['departure'] = np.inf

        # Non-Empty Queue
        else : 
            if self.service_time_type == 'stochastic':
                service_times = time_generator_helper(self.service_obj)
            else :
                service_times = self.mean_service_time
            
            # Schedule The Next Departure
            self.time_next_event['departure'] = self.sim_time + service_times
            self.num_in_q -= 1
            
            # Check if the Entity's Departure is Before Termination Time.
            if self.time_next_event['departure'] <= self.time_next_event['termination']: 
                # Update Statistical Counters
                delay = self.sim_time-self.time_arrival[0]
                self.total_of_delays += delay
                self.num_custs_delayed += 1 

                if service_times + delay >= 4.5 :
                    self.num_custs_wait +=1
                else:
                    pass
            else :
                pass

            # Exit the First Entity in the Queue
            self.time_arrival.pop(0)
            
            # Check the Stopping Criteria
            if  self.stopping_criteria == 'custs_num' and self.num_custs_delayed ==  self.num_delayed_required :
                self.time_next_event['termination'] = self.time_next_event['departure']
            else :
                pass
            


    def report(self):
        """
        Report Method: Display the Results
        """
        self.avg_delay = self.total_of_delays/(self.num_custs_delayed)
        self.pct_custs_wait = (self.num_custs_wait/(self.num_custs_delayed))*100
        self.sys_utilization = self.area_server_status/self.sim_time 
        self.time_avg_num_in_q = self.area_num_in_q/self.sim_time 
        
        print(f'Average Delay: {self.avg_delay}',
              f'Expected Number of Entities in the Queue: {self.time_avg_num_in_q}',
              f'Percentage of Entities Waiting more than 4.5 Minutes in the System: {self.pct_custs_wait}',
              f'System Utilization: {self.sys_utilization}',
              sep='\n')


    def update_time_avg_stats(self):
        """
        Update Time-Continuous Statistical Counters
        """
        self.time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time 
        self.area_num_in_q += self.num_in_q * self.time_since_last_event 
        
        if self.server_status == 'BUSY':
            self.area_server_status += 1 * self.time_since_last_event
        else : 
             self.area_server_status += 0

                
                
