import matplotlib.pyplot as plt
import pandas as pd


def plot_metric(fig,
                ax,
                list_per_event: list,
                label: str,
                marker: str = None,
                log_scale: bool = False,
                ci: bool = False):
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel('Event')
    ax.set_ylabel('Delays')
    ax.grid(True)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()


def plot_metric_with_ci(ax,
                list_per_event: list,
                label: str,
                ci_lower: list,
                ci_upper: list,
                marker: str = None,
                log_scale: bool = False
                ):
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel('Event')
    ax.set_ylabel('Delays')
    ax.grid(True)
    ax.fill_between(list_per_event, ci_lower, ci_upper, alpha = .5)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()
