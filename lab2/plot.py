import os

from matplotlib import pyplot as plt


def create_plot(
    plot_function, data, show=True, save=False, filename=None
):
    plot_function(data)
    if save and filename is not None:
        if os.path.isfile(filename):
            os.remove(filename)
        plt.savefig(f'images/{filename}')
    if show:
        plt.show()


def create_plots(data, plot_to_file_map, show=True, save_to_file=False):
    for plot_function, filename in plot_to_file_map.items():
        create_plot(plot_function, data, show, save_to_file, filename)