import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(data_file='../../baseline.txt', output_path='../../images/', output_name='score_distribution_random_schedules', save=True):
    
    random_scores = []
    with open(data_file) as mytxt:
        for line in mytxt:
            random_scores.append(int(line))

    print(f'The mean is: {np.mean(random_scores)}')
    print(f'smallest score: {np.min(random_scores)}')
    print(f'highest score: {np.max(random_scores)}') 
    
    plt.figure(figsize=(15, 10))
    
    plt.hist(random_scores, bins=50)

    plt.ylabel('Number of random schedules')
    plt.xlabel('Score')
    plt.title("Score distribution of randomly generated schedules")
    plt.show()

    if save:
        plt.savefig(f'{output_path}{output_name}.png', bbox_inches='tight')