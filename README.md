# SIMULATION OF A SINGLE-SERVER QUEUEING SYSTEM
A single-server queueing system is implemented in two different disciplines:<br>
1. First come first serve (FCFS or FIFO)
2. Shortest processing time first (SPT)

The system has two different stopping rules:<br>
1. Number of served Entites 
2. Time Elapsed

The arrival process is modeled as a stochastic Poisson process. Random numbers are generated using the LINEAR CONGRUENTIAL GENERATORS method, and exponential variets are generated using the the Inverse Transform method.


## How to Run:
First, run the following in your terminal to add project root directory to python search path:
```
export PYTHONPATH=${PWD}
```

Then, run the main project script by:
```
python src/run.py
```

## Description:
The model is implemented based on the queueing system assumptions introduced in the following reference.
- The `fcfs.py` is the implementation of FCFS single-server queueing system in OOP paradigm.
- The `spt.py` is the implementation of SPT single-server queueing system in OOP paradigm.
- The `time_generator.py` is the exponential variets generator.
- The `run_simulation.py` is the helper function for running the simulation model. 
- The `result.ipynb` contains the steady-state performance parameters of FCFS and SPT system in M/M/1 and M/D/1, which are computed after 10000 entities are served and 60000 time unit is elapsed. 

## Reference:
Law, A.M.: Simulation Modeling and Analysis, 5th edition. McGraw-Hill, Boston.(2015)
