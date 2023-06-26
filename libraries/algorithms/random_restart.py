from libraries.classes.model import Model
from .hillclimber import HillClimber
from .randomise import Random
from .simulated_annealing import SimulatedAnnealing
from typing import Optional
import sys


def random_restart(
    algorithm: HillClimber | SimulatedAnnealing,
    runs: int = 20,
    temperature: int = 10,
    iterations: int = 2000,
    convergence: int = sys.maxsize,
    mutate_slots_number: int = 1,
    heuristics: Optional[list[str]] = None,
    modifier: int = 1.2,
    verbose: bool = False,
):
    """Random Restart is a meta algorithm for a HillClimber or Simulated Annealing.
    
    The function accepts one of the two algorithms as an argument over which it will
    attempt multiple runs.
    The best performing model is returned after all runs have been performed.
    By randomly generating a new starting model for each run, the HillClimber starts
    in a different valley, which increases the likelihood of climbing a taller peak.
    
    Args:
        runs (int): Amount of runs to be performed. Defaults to 10.
        iterations (int): Amount of iterations for the algorithm. Defaults to 2000.
            Will not be taken into account if convergence argument is passed.
        temperature (int): Temperature for the Simulated Annealing algorithm to start. = 10,
        mutate_slots_number: int = 1,
        convergence: int = sys.maxsize,
        heuristics: Optional[list[str]] = None,
        modifier: int = 1.2,
        verbose: bool = False,
    """
    best_model = Model()
    print('') # Ensure command not overwritten.
    for run in range(runs):
        # Generate a new random model.
        random_model = Random(Model()).run()
        print(
            # Go back 2 lines.
            "\033[A",
            f"Run {run}/{runs}, current penalty score: {best_model.penalty_points}",
            end="\n",
        ) if verbose else None

        # Initialize the algorithm with the correct arguments.
        try:
            exe = algorithm(random_model, temperature)
        except TypeError:
            exe = algorithm(random_model)
        
        # Run the algorithm.
        new_model = exe.run(
            iterations=iterations,
            convergence=convergence,
            mutate_slots_number=mutate_slots_number,
            heuristics=heuristics,
            modifier=modifier,
            verbose=verbose,
        )

        if new_model < best_model:
            # Save the newly generated model if it has a lower score than the old model.
            best_model = new_model

    return model
