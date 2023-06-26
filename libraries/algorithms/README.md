# Algorithms

This package includes several algorithms for problem optimalisation.
BeamSearch, Greedy (and RandomGreedy) are constructive algorithms. HillClimber and Simulated Annealing are iterative algorithms. Random Restart is a meta-algorithm for HillCLimber and Simulated Annealing.

All algorithms are dependant on a functional Model class to manipulate.

## Table of Contents

* [beam_search.py](#beam_search.py)
* [greedy.py](#greedy.py)
* [The HillClimber family](#the-hillclimber-family)
    * [hillclimber.py](#hillclimber.py)
    * [random_restart.py](#random_restart.py)
    * [simulated_annealing.py](#simulated_annealing.py)

## [beam_search.py](/libraries/algorithms/beam_search.py)
The beam search algorithm is usually a breadth first algorithm with a priority queue and a limit (beam) on the number of child states that will be created. In this project, the beam search is closer to a depth first algorithm with a priority queue and beam (n) because the state space of this case is too extensive for a breadth first algorithm.

The beam search picks a timeslot and location (index) based on highest capacity available and 1 out of 3 times randomly. For this index, n activities are selected based on the chosen heuristic. The default heuristic is "random", where activities are picked randomly. The other two heuristics are "capacity" where activities are selected based on their capacity and its match to the index capacity, and "totalpenalty" where activities are selected based on the total penalty they cause in the timetable.

## [greedy.py](/libraries/algorithms/greedy.py)

The greedy module contains both a deterministic Greedy and a random Greedy.

## The HillClimber Family

The HillClimber family all function in the same manners as they are child and parent classes of eachother. The Random Restart is a meta-algorithm which gives eiter HillClimber or Simulated Annealing a randomly generated model for each new run. Running HillClimber or Simulated Annealing on their own requires a valid (filled in) timetable. 

Multiple toggles are possible for running the algorithms. It is possible to adjust the number of iterations, the number of swaps each iteration, to evaluate based on convergence, and a number of heuristics.

Available heuristics:
* Centre placement: Increases the likelihood of swapping activities with high penalties outside of the centre timeslots (11 am and 1 pm) to an index in the centre.
* Balancing: Increases the likelihood of swapping an activity causing a high penalty to an index with a low penalty.
* Day placement: Increases the likelihood of moving activities from days with a high number of activity overlap for students towards days with a high number of gap hours for students.

It is posible to run a combination of heuristics.

### [hillclimber.py](/libraries/algorithms/hillclimber.py)

In addition to the family options, it is also possible to run the HillClimber in a deterministic manner. This results in a Steepest Ascend HillClimber. With no options adjusted, it functions as a stochastic HIllClimber.

### [simulated_annealing.py](/libraries/algorithms/simulated_annealing.py)

The Simulated Annealing algorithm is a child of the HillClimber and utilizes a cooling scheme to allow a greater search in the state space. Options for the cooling scheme are linear progression and exponential progression.

### [random_restart.py](/libraries/algorithms/random_restart.py)

The random restart algorithm runs on top of the two other algorithms and allows for comparison between different runs of the HillClimber. It attempts to search a greater statespace in comparison to both the HillCLimber and the Simulated Annealing.


