from libraries.classes.model import Model
from libraries.helpers.random_restart_to_csv import to_csv
from .hillclimber import HillClimber
from .randomise import Random
from .simulated_annealing import SimulatedAnnealing
from typing import Optional
import random
import sys
import os
import time


def random_restart(
    algorithm: HillClimber | SimulatedAnnealing,
    seed: int = 0,
    runs: int = 20,
    temperature: int = 1,
    iterations: int = 2821,
    convergence: int = sys.maxsize,
    mutate_slots_number: int = 1,
    heuristics: Optional[list[str]] = None,
    modifier: float = 1.5,
    verbose: int = 0,
    save: bool = False,
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
        runs (int): Amount of runs to be performed. Defaults to 20.
        iterations (int): Number of iterations for the Hillclimber to 'climb'.
            Defaults to 2821 iterations.
        temperature (int): Startin temperature for simulated annealing. Defaults to 1.
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
        modifier (float): Effect a heuristic has on the heat map. Defaults to a multiplier of 1.5.
        verbose (int): Evaluate if current run and score found is printed.
            Defaults to 0, in which none is printed. at 1, only run is printed.
            On 2, algorithm verbosity is also added.
        save (bool): Evaluate if generated models are to be stored. Defaults to False.
            Will store files in /libraries/results/random_restart/<class algorithm version> model and scores.
    """
    random.seed(seed)
    best_model = Model()

    verbosity = True if verbose >= 2 else False
    print(f"Starting PID Number {os.getpid()}")
    print("")  # Ensure command not overwritten.
    for run in range(runs):
        start_time = time.time()
        # Generate a new random model.
        random_model = Random(Model()).run()
        print(
            "\033[A",  # Go back 2 lines.
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

        if new_model < best_model:
            # Save the newly generated model if it has a lower score than the old model.
            best_model = new_model

        if save is True:
            # Store the generated models and their data in memory.
            to_csv(new_model, end_time, run, scores, f"{exe}")

    return best_model
