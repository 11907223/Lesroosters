# Algorithms

This package includes several algorithms for problem optimalisation.
BeamSearch, Greedy (and RandomGreedy) are constructive algorithms. HillClimber and Simulated Annealing are iterative algorithms. Random Restart is a meta-algorithm for HillCLimber and Simulated Annealing.

All algorithms are dependent on a functional Model class to manipulate.

## Table of Contents

* [beam_search.py](#beam_search.py)
* [greedy.py](#greedy.py)
* [The HillClimber family](#the-hillclimber-family)
    * [hillclimber.py](#hillclimber.py)
    * [random_restart.py](#random_restart.py)
    * [simulated_annealing.py](#simulated_annealing.py)

## [beam_search.py](/libraries/algorithms/beam_search.py)
The beam search algorithm is usually a breadth first algorithm with a priority queue and a limit (beam) on the number of child states that will be created. In this project, the beam search is implemented as a depth first algorithm because the state space of this case is too extensive for a breadth first algorithm. The priority of states in the queue is calculated through total penalty points and the number of unassigned activities of the state.

Available heuristics:
* Random: activities are randomly picked
* Capacity: activities are selected according to their capacity and if they closely match the capacity of the lecture hall.
* Total penalty: activities are selected so that they result in the lowest possible penalty points for the schedule.

## [greedy.py](/libraries/algorithms/greedy.py)

The greedy module contains the "Greedy" and "RandomGreedy" classes, used to run constructive algorithms that generate a schedule from an empty model, by gradually inserting activities into it.
The greedy algorithm inserts the activities step-by-step at the index that minimizes the total amount of penalty points the most.
RandomGreedy is a subclass of Greedy that works similarly, but occasionally inserts an activity at a random index instead of the "best", based on a probability that decays exponentially as the run progresses. 

Heuristics:
* The exponential function was used to prevent an random insertion at the end of a run, which could cause significant amount of gap penalties that can not be 'corrected' by greedy choices anymore. The parameters of the exponential function are set to start of with a 0.7 probability of random insertion and decrease so that it will be 10% of that at the halfway mark (0.07). 
* RandomGreedy considers room size when inserting an activity, to prevent unnecessary capacity penalties.
* sort (optional): sorts activities to be inserted from largest to smallest.
* sort_overlap (optional): sorts activities to be inserted on amount of overlap, from most to least.
* shuffle (optional): randomly shuffles the list of activities to be inserted.

## The HillClimber Family

The HillClimber family all function in the same manners as they are child and parent classes of eachother. The Random Restart is a meta-algorithm which gives eiter HillClimber or Simulated Annealing a randomly generated model for each new run. Running HillClimber or Simulated Annealing on their own requires a valid (filled in) timetable.

Multiple toggles are possible for running the algorithms. It is possible to adjust the number of iterations, the number of swaps each iteration, to evaluate based on convergence, and a number of heuristics.

Available heuristics:
* Centre placement: Increases the likelihood of swapping activities with high penalties outside of the centre timeslots (11 am and 1 pm) to an index in the centre.
* Balancing: Increases the likelihood of swapping an activity causing a high penalty to an index with a low penalty.
* Day placement: Increases the likelihood of moving activities from days with a high number of activity overlap for students towards days with a high number of gap hours for students.

It is possible to run a combination of heuristics.

### [hillclimber.py](/libraries/algorithms/hillclimber.py)

In addition to the family options, it is also possible to run the HillClimber in a deterministic manner. This results in a Steepest Ascend HillClimber. With no options adjusted, it functions as a stochastic HIllClimber.

### [simulated_annealing.py](/libraries/algorithms/simulated_annealing.py)

The Simulated Annealing algorithm is a child of the HillClimber and utilizes a cooling scheme to allow a greater search in the state space. Options for the cooling scheme are linear progression and exponential progression.

### [random_restart.py](/libraries/algorithms/random_restart.py)

The random restart algorithm runs on top of the two other algorithms and allows for comparison between different runs of the HillClimber. It attempts to search a greater statespace in comparison to both the HillCLimber and the Simulated Annealing.