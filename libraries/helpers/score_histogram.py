import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss 

def plot_histogram(data_file='../../results/baseline.txt', output_path='../../images/', output_name='score_distribution_random_schedules', save=True):
    
    random_scores = []
    random_scores = np.loadtxt(data_file, dtype=int)

    print(f'The mean is: {np.mean(random_scores)}')
    print(f'smallest score: {np.min(random_scores)}')
    print(f'highest score: {np.max(random_scores)}') 
    
    plt.figure(figsize=(15, 10))

    n_bins = int(2 * np.log(len(random_scores) / np.log(2) + 1)) # Sturges' formula
    result = plt.hist(random_scores, bins=n_bins, color='royalblue')

    plt.ylabel('Number of random schedules', fontsize=16)
    plt.xlabel('Score', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title("Score distribution of randomly generated schedules", fontsize=18)

    # plot gaussian    
    mean     = np.mean(random_scores)
    variance = np.var(random_scores)
    sigma    = np.sqrt(variance)
    x  = np.linspace(min(random_scores), max(random_scores), 100)
    dx = result[1][1] - result[1][0]
    scale = len(random_scores)*dx
    plt.plot(x, ss.norm.pdf(x, mean, sigma)*scale, 'r-', linewidth=3)
    
    if save:
        plt.savefig(f'{output_path}{output_name}.png', bbox_inches='tight')