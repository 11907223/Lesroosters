# Algorithms

## Table of Contents

## Beam Search
The beam search algorithm is usually a breadth first algorithm with a priority queue and a limit (beam) on the number of child states that will be created. In this project, the beam search is closer to a depth first algorithm with a priority queue and beam (n) because the state space of this case is too extensive for a breadth first algorithm.

The beam search picks a timeslot and location (index) based on highest capacity available and 1 out of 3 times randomly. For this index, n activities are selected based on the chosen heuristic. The default heuristic is "random", where activities are picked randomly. The other two heuristics are "capacity" where activities are selected based on their capacity and its match to the index capacity, and "totalpenalty" where activities are selected based on the total penalty they cause in the timetable.