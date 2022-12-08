import matplotlib.pyplot as plt

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
    ax.set_ylabel('Delays (time unit)')
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
    ax.set_ylabel('Delays (time unit)')
    ax.grid(True)
    # plot confidence interval
    ax.fill_between([x for x in range(len(list_per_event))], ci_lower, ci_upper, alpha = .5, label = f'{label_} confidence interval 95%')
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()