from utils import *
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from collections import OrderedDict

def plot_metric(fig,
                ax,
                list_per_event: list,
                label: str,
                marker: str = None,
                log_scale: bool = False,
                x_label = 'Event'
                ):
    
    '''
    This function plot a generic array of delays with standard functions of matplotlib.pyplot when a confidence interval 
    is not requested
    '''
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Probability')
    ax.grid(True)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()


def plot_metric_with_ci(ax,
                list_per_event: list,
                label_: str,
                ci_lower: list,
                ci_upper: list,
                x_label = 'Event',
                marker: str = None,
                log_scale: bool = False
                ):
    '''
        This function plot a generic array of delays with standard functions of matplotlib.pyplot
        when a confidence interval is requested
    '''
    ax.plot(list_per_event, label = label_, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Probability')
    ax.grid(True)
    # plot confidence interval
    ax.fill_between([x for x in range(len(list_per_event))], ci_lower, ci_upper, alpha = .5, label = f'{label_} confidence interval 95%')
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()

def prob_confidence_interval(
        p: float,
        confidence: float,
        k: int
        ) -> tuple[float, float]:
    z = stats.norm.ppf(q=(1-confidence)/2)
    s_hat = np.sqrt(p*(1-p)/k)
    return (p - z*s_hat, p + z*s_hat)

class SeedGenerator:
    def __init__(
            self,
            k: int,
            seed: int):
        self.generator = np.random.default_rng(seed=seed)
        self.low = k
        self.high = k**3
    
    def __call__(self) -> int:
        return self.generator.integers(
            low=self.low,
            high=self.high
            )

lam = [0.6, 0.8, 0.9, 0.95, 0.99, 1.01, 1.05, 1.1, 1.3]
RUNS = 1000
confidence = 0.90

if __name__ == '__main__':
    for l in lam:
        print(f'lambda: {l}')
        extinsions = 0
        n_nodes = list()
        non_extinsion_counter = 0
        last_generations = dict()
        infinite_counter = 0
        extinction_probabilities = list()
        confidence_intervals_lower = list()
        confidence_intervals_upper = list()
        theoretical_extinsion_probs = list()
        children = dict()
        normalized_values = list()

        get_seed = SeedGenerator(
        seed=42,
        k = RUNS
        )
        for _ in range(RUNS):
            # instanciate the simulator
            simulator = GWProcess(30, l, get_seed())
            # Execute the simulation
            last_generation, children_per_generation = simulator.execute()
            
            # if the tree is not infinite
            if last_generation > 0:
                # increase a counter w.r.t. the last detected generation which is the one before the extinction
                if last_generation not in last_generations.keys():
                    last_generations[last_generation] = 1
                else:
                    last_generations[last_generation] += 1
                # count the number of individuals per generation
                for i in range(len(children_per_generation)):
                    if i not in children.keys():
                        children[i] = children_per_generation[i]
                    else: 
                        children[i] += children_per_generation[i]
            else:
                infinite_counter += 1
        # sort the dictionary
        last_generations = OrderedDict(sorted(last_generations.items()))
        print(f'probability of infinite trees for lambda = {l}: ',infinite_counter/RUNS)
        # remove the last generation which is the one with 0 individuals
        last_generations.popitem()
        generations = last_generations.keys()
        # compute the MGF for all the generations from 0 to the highest one
        max_generation = max(generations)
        theoretical_extinsion_probs.append(np.exp(-l))
        for i in range(max_generation):
            prev_prob = theoretical_extinsion_probs[-1]
            theoretical_extinsion_probs.append(np.exp(-l*(prev_prob-1)))
        for val in last_generations.values():
            # compute the probability as the number of extinctions devided by the number of trials
            prob = val/RUNS
            extinction_probabilities.append(prob)
        probs = np.cumsum(extinction_probabilities)
        for p in probs:
            ci = prob_confidence_interval(p, confidence, RUNS)
            confidence_intervals_lower.append(ci[0])
            confidence_intervals_upper.append(ci[1])
        for val in children.values():
            # take the average number of individuals per generation w.r.t. the number of trials
            normalized_values.append(val/RUNS)
        if l == 0.8:
            fig, ax = plt.subplots()
            ax.bar([i for i in range(len(normalized_values))],normalized_values)
            ax.set_xlabel('generation')
            ax.set_ylabel('number of individuals')
            plt.savefig(f'graphs/histogram with lambda = 0.8.png')
        fig, ax = plt.subplots()
        ax.plot(theoretical_extinsion_probs, label = 'theoretical extinction probability')
        plot_metric_with_ci(ax, probs, 'emprical probability of extinction',confidence_intervals_lower, confidence_intervals_upper, 'generation')
        fig.suptitle(f'Poisson parameter = {l}')
        plt.savefig(f'graphs/generation vs probabilities. L = {l}.png')
        plt.close()