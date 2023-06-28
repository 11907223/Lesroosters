from libraries.classes.model import Model
from .hillclimber import HillClimber
from .randomise import Random
from .simulated_annealing import SimulatedAnnealing
from typing import Optional
import random
import sys
import os
import pickle
import time
import csv

def random_restart(
    algorithm: HillClimber | SimulatedAnnealing,
    seed: int = 0,
    runs: int = 20,
    temperature: int = 1,
    iterations: int = 2812,
    convergence: int = sys.maxsize,
    mutate_slots_number: int = 1,
    heuristics: Optional[list[str]] = None,
    modifier: float = 1.5,
    verbose: int = 0,
    store_runs: bool = False,
):
    """Random Restart is a meta algorithm for a HillClimber or Simulated Annealing.

    The function accepts one of the two algorithms as an argument over which it will
    attempt multiple runs.
    The best performing model is returned after all runs have been performed.
    By randomly generating a new starting model for each run, the HillClimber starts
    in a different valley, which increases the likelihood of climbing a taller peak.

    The arguments to this function are the same as the arguments given to one of the two algorithms.

    Args:
        algorithm (HillClimber | Simulated Annealing): Algorithm to be used.
        seed (int): Seed to be used for the random library. Defaults to 0.
        runs (int): Amount of runs to be performed. Defaults to 10.
        iterations (int): Number of iterations for the Hillclimber to 'climb'.
            Defaults to 2000 iterations.
        temperature (int): Startin temperature for simulated annealing. Defaults to 10.
        convergence (bool): Evaluate if iterations are based on convergence.
            If no value is given, convergence is not evaluated.
        mutate_slots_number (int): Number of mutations to occur each iteration.
            Defaults to 1 mutation per iteration.
        heuristics (list[str]): Optional list of heuristics to be used. Heuristics can be combined.
            Options are:
                'balance': Use weighted swapping to trade indices with a
                    penalty score to an index with a lower penalty score,
                'middle': Use weighted swapping to trade indices with
                    high penalty scores towards the centre of the schedule (timeslot 11 & 1),
                'days': Use weighted swapping to trade days containing
                    high gap penalties with days containing high conflict hour penalties.
                'steepest': Evaluate if algorithm has to only take each steepest climb.
                    Will result in deterministic algorithm behaviour.
        modifier (float): Effect a heuristic has on the heat map. Defaults to a multiplier of 1.8.
        verbose (int): Evaluate if current run and score found is printed.
            Defaults to 0, in which none is printed. at 1, only run is printed.
            On 2, algorithm verbosity is also added.
        store_runs (bool): Evaluate if each run score is to be stored. Defaults to false.
            If true, will return a list of scores 
    """
    random.seed(seed)
    scores: list[int] = []
    best_model = Model()

    verbosity = True if verbose >= 2 else False
    print(f"Starting {os.getpid()}")
    print("")  # Ensure command not overwritten.
    for run in range(runs):
        start_time = time.time()
        # Generate a new random model.
        random_model = Random(Model()).run()
        print(
            "\033[A", # Go back 2 lines.
            f"Run {run}/{runs}, current penalty score: {best_model.penalty_points}",
            end="\n",
        ) if verbose >= 1 else None

        # Initialize the algorithm with the correct arguments.
        try:
            exe = algorithm(random_model, temperature)
        except TypeError:
            exe = algorithm(random_model)

        # Run the algorithm.
        new_model, scores = exe.run(
            iterations=iterations,
            convergence=convergence,
            mutate_slots_number=mutate_slots_number,
            heuristics=heuristics,
            modifier=modifier,
            verbose=verbosity,
        )
        end_time = time.time() - start_time

        scores.append(new_model.penalty_points)
        if new_model < best_model:
            # Save the newly generated model if it has a lower score than the old model.
            best_model = new_model
        with open(f'{algorithm} models.pkl', 'ab+') as file:
            pickle.dump(new_model, file, pickle.HIGHEST_PROTOCOL)
        with open(f"{algorithm} scores.csv", 'a+', newline='') as score_file:
            csv.writer(score_file).writerow((round(end_time, 3), new_model.penalty_points, scores))

    if store_runs is True:
        # Enables averaging of scores over runs for tuning and comparison of heuristics.
        return scores
    return best_model
