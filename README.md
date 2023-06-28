# Lectures & Lesroosters

## Table of Contents

* [Introduction](#introduction)
* [Project Overview](#project-overview)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Project Summary](#project-summary)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## Introduction
This project aims to generate an optimal university timetable. It is based on the University Timetabling Problem. As an [NP-Hard problem](https://en.wikipedia.org/wiki/NP-hardness), there is no solution that solves the problem in polynomial time. It is currently possible to acquire an approximation of an optimal solution. This is done through several optimalisation algorithms.

The results of several runs of the algorithms can be found in the results folder. This project provides insights and visualisations of choices to be made for problem optimalisation. The results and findings can be used for further optimalisation of algorithms to approach an optimal schedule.

## Project Overview
Data stems from the University of Amsterdam Computer Science track. The timetabling problem tackled in this project contains 29 courses, 609 students and 7 locations. In order to solve this case, several algorithms are used to create the optimal timetable. The following algorithms are used for problem optimalisation:
* Greedy
* Random-Greedy
* Beam Search
* Hill Climber
    - Steepest Ascend
    - Stochastic
    - Random-Restart (Meta-algorithm)
* Simulated Annealing

## Installation

### Prerequisite requirements.
Python version 3.10.6.
tkinter version 8.6


1. Installation of tkinter:
```bash
sudo apt-get install python3-tk
```


2. Clone the repository:
```bash
git clone https://github.com/11907223/lesroosters
```
3. Navigate to the project root directory.
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The algorithms are run via the terminal.

Structure of command line argument:
```bash
python3 main.py [algorithm] [--help] [-n N] [-hr HR] [-s] [-v]
```
`algorithm` is the only mandatory argument and must be one of the following: [random, beam_search, hillclimber, simulated_annealing, greedy, random_greedy]

`-hr` is used to pass used heuristics in the specified run(s). The options for this argument per algorithm are listed in the paragraphs below.

`-n` is used to pass the number of runs (default is 1).

`-s` saves the results to a csv.

`-v` visualizes the schedule in a pop-up visualizing when runs are finished.

### random

The random algorithm uses no heuristics. Passing an argument to --hr when running random will not alter the run in any way.

To run random 100 times:
```bash
python3 main.py random -n 100
```

### baseline
To run random 1000 times: 
```bash
python3 main.py baseline -n 10
```
Note that for the baseline, the number of runs it executes will be the value passed through `-n`, multiplied by 100. 

### Greedy and RandomGreedy

Three different types of heuristics can be selected. The heuristics determine the order in which the activities are inserted into the schedule.

 - **sort_size** inserts activities from biggest to smallest (i.e. from most students to least students).
 - **sort_overlap** inserts activities from most overlap with other activites to least. 
 - **shuffle** randomly shuffles the order in which activities inserted.

Only one heuristic can be selected at a time for greedy and random_greedy. If multiple are provided, only the first will be applied. If no heuristic or incorrect heuristic is given, activities will be inserted in the order they were listed in in the data files.

Note that greedy can only run more than once when shuffle is selected, since the other methods run deterministically.

To run RandomGreedy three times with shuffle heuristic.
```bash
python3 main.py random_greedy -n 3 -hr shuffle
```

### SimulatedAnnealing and HillClimber

Combinations may be made between three different heuristics.
- **day** activities on high penalty days are moved to days with lower total penalty.
- **middle** activities with high scores are moved towards the middle of the day.
- **balance** activities with high scores are swapped with activities with low scores.

Either one, combinations of two, or all heuristics can be selected for a hillclimber or simulated annealing run.

To run SimulatedAnnealing five times with heuristics day and middle and save the results:
```bash
python3 main.py simulated_annealing -n 5 -hr day middle -s
```

### BeamSearch
Only one of the following heuristics can be selected at a time for beam search.

- **capacity** selects activities that fit best when considering the capacity of the hall.
- **total penalty** selects activities that give lowest total penalty.
- **random (default)** selects activities randomly.

To run beam search once and save and visualize the results:
```bash
python3 main.py beam_search -s -v
```

For a summary on the usage of main.py and its commandline arguments, run:
```bash
python3 main.py -h
```

## Project Structure

- [libraries:](libraries/) Contains all the code to run main.py.
    - [algorithms:](/libraries/algorithms/) Contains all the algorithm classes.
    - [classes:](/libraries/classes/) Contains all the static classes representing data and the model class.
    - [helpers:](/libraries/helpers/) Contains all the helper functions.
        - [experiments:](/libraries/helpers/experiments/) Contains scripts to perform a tuning experiment with hillclimber.
- [data:](/data/) Contains all data in csv files and data analysis in a jupyter notebook.
- [results:](/results/) This is where are the results from algorithms run via the CLI are stored.
- [images:](/images/) Contains image files of results and UML.
- [requirements.txt](/requirements.txt) Lists the required Python packages and their versions.


## Project Summary

In this project various algorithms were tested under a limited amount of time to optimize the university scheduling problem.
As a constraint-optimization problem, the goal was to minimize the number of penalty points assigned to a timetable.


In this project, it has been discovered that with a limited amount of processing time, the Randomized-Greedy Algorithm forms the most optimized problem in 211 seconds. This is a deterministic optimization algorithm. By applying a heuristic of minimizing the number of overlapping classes of students, it made a schedule with a total of 344 of which 309 can be attributed to penalty points due to conflict. Schedule gap penalties accounted for just 14 penalty points, and 1 penalty point was given for a single activity being 1 person over capacity. 20 penalty points were given for activities occupying the evening slots.

It is possible to reduce potential conflict penalties by increasing the number of different activities. By splitting lectures into two groups (lecture 1a and 1b), students can be at their respective activities without having a requirement of being at two places at the same hour. Currently the schedule is filled for 72 out of 145 slots. By making use of more timeslots, it is possible that created schedules reduce the number of overlapping activities for students. 

> *click the image for a complete overview*

 [![img](/images/screenshot_greedy_schedule.png)](/images/greedy_schedule.txt)
 


There is the fact that a university timetable has a development span of 1 semester. This means that it is likely that more optimal solutions can be developed with different algorithms that better utilize that time.

## Acknowledgements
This project was performed by Niels Huang, Nina van der Meulen en Elise van Iterson.

Special thanks to Quinten van der Post and Moos Middelkoop for guiding us through this process.

## Contact
Inquiries about the project can be mailed to niels.huang@student.uva.nl