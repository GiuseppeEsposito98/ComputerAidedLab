import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.stats as st
from typing import *


def compute_ci(y_list: List[List[float]]):
    lower_bound, upper_bound = list(), list()
    for lst in y_list:
        ci = st.t.interval(alpha = 0.05, df = len(y_list)-1, loc = np.mean(lst), scale = np.std(lst))
        lower_bound.append(ci[0])
        upper_bound.append(ci[1])
    return np.array(lower_bound), np.array(upper_bound)

def compute_mean_line(y_list):
    list_ = list()
    counter = 0
    for lst in y_list:
        list_.append(np.mean(lst))
        counter +=1 
    return np.array(list_)

def setup_save_plot(fig,
                ax,
                x_label:str='',
                y_label:str='',
                label_:str='',
                scale:str='',
                save_flag:bool=True,
                filename:str=''):
    output_path= os.path.join('graphs',filename)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.suptitle(label_)
    ax.grid()
    ax.legend()
    if scale!='':
        ax.set_xscale(scale)
        ax.set_yscale(scale)
    if save_flag:
        output_path = os.path.join('graphs',filename)
        plt.savefig(output_path)
    

def prob_confidence_interval(
        p: float,
        confidence: float,
        k: int
        ) -> tuple[float, float]:
    z = st.norm.ppf(q=(1-confidence)/2)
    s_hat = np.sqrt(p*(1-p)/k)
    return (p - z*s_hat, p + z*s_hat)


def plot_avgs(ax,
                fig,
                x_list: list(),
                y_list: List[List[float]],
                theor_values: float = None,
                x_label:str='',
                y_label:str='',
                scale:str='',
                need_ci:bool=False,
                label_:str='',
                save_flag:bool=True,
                filename:str=''):
    '''
    Plot average minimum number of extractions with respect to possible extraction
    '''

    if need_ci:
        lower_bound, upper_bound = compute_ci(y_list=y_list)
        arr = compute_mean_line(y_list)
        ax.fill_between(x_list,arr+lower_bound,arr+upper_bound,alpha=.5, label = "confidence interval 95%")
    else: 
        arr = np.array(y_list)
    if theor_values != None:
        label_ = 'empirical'
        ax.plot(x_list, theor_values, color = 'r', label = "theoretical", marker = None)
    ax.plot(x_list, arr, label=label_, marker = ".")
    setup_save_plot(fig, ax, x_label, y_label, label_, scale, save_flag, filename)
    