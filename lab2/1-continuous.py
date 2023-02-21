import numpy as np
from numpy.random import rand, seed
import matplotlib
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
        f"The values are {random_values}"
        f"The mean of the data is {mean:.4f}"
        f"The standard deviation of the data is {standard_deviation:.4f}"
        f"The first quartile is {first_quartile:.4f}"
        f"The third quartile is {third_quartile:.4f}"
        f"The median is {median:.4f}"
    )
    return random_values


def organize(data):
    plt.hist(data, bins=8)
    plt.xlabel('Values')
    plt.ylabel('Occurrence')
    plt.title('Histogram of the random variable, 8 bins')
    plt.show()

    plt.hist(data, bins=5)
    plt.xlabel('Values')
    plt.ylabel('Occurrence')
    plt.title('Histogram of the random variable, 5 bins')
    plt.show()


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


def plot(data):
    plt.boxplot(data)
    plt.xlabel('Distribution')
    plt.ylabel('Values')
    plt.title('Boxplot of the random variable')
    plt.show()

    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1
    num_outliers = len(data[data < q1 - 1.5 * iqr]) + len(data[data > q3 + 1.5 * iqr])
    print(f"The number of potential outliers is {num_outliers}.\n")


def compare(data):
    print(
        "The first quartile is slightly lower than expected.\n"
        "The median is slightly lower than expected.\n"
        "The third quartile is slightly lower than expected.\n"
        f"The minimum has to be at least 0, but is inevitably higher "
        f"({data.min()}) due to the relatively small amount of points.\n"
        f"The maximum has to be at most 1, but is inevitably lower "
        f"({data.max()}) due to the relatively small amount of points.\n"
        f"The inter-quartile range is slightly lower than expected.\n"
        f"The overall shape of the histogram is flat but not complerely, "
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
    organize(data)
    describe()
    describe_theoretical()
    plot(data)
    compare(data)
