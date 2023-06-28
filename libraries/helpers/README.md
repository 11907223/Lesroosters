# Helpers

This package includes all helper functions for the project.


## Table of Contents

* [Experiments](#experiments)
* [load_data.py](#load_data.py)
* [print_results.py](#print_results.py)
* [save_greedy_run.py](#save_greedy_run.py)
* [score_histogram.py](#score_histogram.py)
* [visualize.py](#visualize.py)

## [Experiments](/libraries/helpers/experiments/)

This folder contains tuner modules for HillClimber and Simulated Annealing.
The temperature, number of iterations and the modifier of heuristical weight are tuned.

Usage:
```bash
python3 experiments/random_restart_tuning.py
```
> Warning: This takes a very long time to execute.

## [load_data.py](/libraries/helpers/load_data.py)

This file contains functions to read all course, student, and location data from csv files.

Functions:
* load_courses
* load_students
* load_halls
* _load_subjects
* _update_course

## [print_results.py](/libraries/helpers/print_results.py)

This file contains a function to print the results of a model in a nice format.

Function:
* print_results

## [save_greedy_run.py](/libraries/helpers/save_greedy_run.py)

This file contains a function save the results of the greedy algorithm to a csv.

Function:
* to_csv

## [score_histogram.py](/libraries/helpers/score_histogram.py)

This file contains a function to plot the baseline results to a histogram.

Function:
* plot_histogram

## [visualize.py](/libraries/helpers/visualize.py)

This file contains functions to visualize a model with tkinter in a pop up window.

Functions:
* create_df
* tkinter_pop_up
* visualize_schedule
