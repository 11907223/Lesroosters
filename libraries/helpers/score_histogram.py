import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss 

def plot_histogram(data_file='../../baseline.txt', output_path='../../images/', output_name='score_distribution_random_schedules', save=True):
    
    random_scores = []
    with open(data_file) as mytxt:
        for line in mytxt:
            random_scores.append(int(line))

    print(f'The mean is: {np.mean(random_scores)}')
    print(f'smallest score: {np.min(random_scores)}')
    print(f'highest score: {np.max(random_scores)}') 
    
    plt.figure(figsize=(15, 10))
    
    result = plt.hist(random_scores, bins=70, color='royalblue')[0:len(random_scores)-1000]

    plt.ylabel('Number of random schedules', fontsize=16)
    plt.xlabel('Score', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title("Score distribution of randomly generated schedules", fontsize=18)

    # gaussian    
    mean     = np.mean(random_scores)
    variance = np.var(random_scores)
    sigma    = np.sqrt(variance)
    x  = np.linspace(min(random_scores), max(random_scores), 100)
    dx = result[1][1] - result[1][0]
    scale = len(random_scores)*dx
    plt.plot(x, ss.norm.pdf(x, mean, sigma)*scale, 'r-', linewidth=3)
    
    if save:
        plt.savefig(f'{output_path}{output_name}.png', bbox_inches='tight')