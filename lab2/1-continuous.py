import os

import numpy as np
from numpy.random import rand, seed
import matplotlib.pyplot as plt


SIZE = 50


def collect(size=SIZE):
    random_values = rand(size)
    mean = random_values.mean()
    standard_deviation = random_values.std()
    first_quartile = np.quantile(random_values, 0.25)
    third_quartile = np.quantile(random_values, 0.75)
    median = np.median(random_values)
    print(
        f"The values are {random_values}\n"
        f"The mean of the data is {mean:.4f}\n"
        f"The standard deviation of the data is {standard_deviation:.4f}\n"
        f"The first quartile is {first_quartile:.4f}\n"
        f"The third quartile is {third_quartile:.4f}\n"
        f"The median is {median:.4f}\n"
    )
    return random_values


def _create_plot(
    plot_function, data, show=True, save=False, filename=None
):
    plot_function(data)
    if save and filename is not None:
        if os.path.isfile(filename):
            os.remove(filename)
        plt.savefig(f'images/{filename}')
    if show:
        plt.show()


def create_plots(data, show=True, save_to_file=False):
    PLOT_TO_FILE_MAP = {
        _plot_histogram_with_8_bins: 'histogram-8-bin.png',
        _plot_histogram_with_5_bins: 'histogram-5-bin.png',
        _create_boxplot: 'boxplot.png',
    }
    for plot_function, filename in PLOT_TO_FILE_MAP.items():
        _create_plot(plot_function, data, show, save_to_file, filename)


def _plot_histogram_with_n_bins(data, n):
    plt.hist(data, bins=n)
    plt.xlabel('Values')
    plt.ylabel('Occurrence')
    plt.title(f'Histogram of the random variable, {n} bins')


def _plot_histogram_with_8_bins(data):
    _plot_histogram_with_n_bins(data, n=8)


def _plot_histogram_with_5_bins(data):
    _plot_histogram_with_n_bins(data, n=5)


def describe():
    print(
        "The first graph should be flat, since we sampled from a "
        "uniform distribution. However, since there are only 50 "
        "data points, and 8 bins. the histogram looks more irregular. "
        "The second graph looks more flat, since there are fewer bins."
    )


def describe_theoretical():
    print(
        "The random variable has a uniform distribution "
        "with parameters 0 and 1."
    )
    print(
        "The mean of the data is 0.5\n"
        "The standard deviation of the data is 0.33\n"
        "The first quartile is 0.25\n"
        "The third quartile is 0.75\n"
        "The median is 0.5\n"
    )
    print(
        "The empirical and the theoretical values are not "
        "very close since the amount of sampled points is "
        "relatively low."
    )


def boxplot_outliers(data):
    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1
    num_outliers = (
        len(data[data < q1 - 1.5 * iqr])
        + len(data[data > q3 + 1.5 * iqr])
    )
    print(f"The number of potential outliers is {num_outliers}.\n")


def _create_boxplot(data):
    plt.boxplot(data)
    plt.xticks([])
    plt.xlabel('Distribution')
    plt.ylabel('Values')
    plt.title('Boxplot of the random variable')


def compare(data):
    print(
        "The first quartile is slightly lower than expected.\n"
        "The median is slightly lower than expected.\n"
        "The third quartile is slightly lower than expected.\n"
        f"The minimum has to be at least 0, but is inevitably higher "
        f"({data.min():.4f}) due to the relatively small amount of points.\n"
        f"The maximum has to be at most 1, but is inevitably lower "
        f"({data.max():.4f}) due to the relatively small amount of points.\n"
        f"The inter-quartile range is slightly lower than expected.\n"
        f"The overall shape of the histogram is flat but not completely, "
        f"due to the relatively small amount of points.\n"
    )
    print(
        "Since we are dealing with a uniform distribution, ideally "
        "the boxplot should have 4 equal parts, two inside the box "
        "plus the two tail ends. In reality, the boxplot is more skewed, "
        "with lower values than expected.\n"
    )


if __name__ == '__main__':
    seed(42)
    np.set_printoptions(
        formatter={'float': lambda x: '{0:0.4f}'.format(x)}
    )
    # matplotlib.use('TkAgg')

    data = collect()
    describe()
    describe_theoretical()
    boxplot_outliers(data)
    compare(data)
    create_plots(data, save_to_file=True)
