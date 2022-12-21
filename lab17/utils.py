import hashlib
import matplotlib.pyplot as plt

def compute_fingerprint(n, word):
        # compute the hash of a given string using md5 on a range [0,n-1]
        word_bytes = hashlib.md5(word.encode('utf-8')) # md5 hash
        word_hash_int = int(word_bytes.hexdigest(), 16) # md5 hash in integer format
        h = word_hash_int % n # map into [0,n-1]
        return h

def plot_metric(ax, x_metric, y_metric, output_path, x_label, y_label, x_log_scale_flag = False, y_log_scale_flag= False, save_flag = True):
        ax.plot(x_metric, y_metric)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if save_flag:
            plt.savefig(output_path)
        if x_log_scale_flag:
            ax.set_xscale('log')
        if y_log_scale_flag:
            ax.set_yscale('log')