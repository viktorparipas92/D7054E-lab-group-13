import pandas as  pd
import statistics
recipe_headers = ["Recipe", "X"]
recipe_rows = [[1,1],[2,5],[3,2],[4,5],[5,6],[6,1],[7,2],[8,6],[9,5],[10,2],[11,5],[12,1],[13,1],[14,3],[15,2],[16,2],[17,2],[18,4],[19,6],[20,1],[21,6],[22,5],[23,2],[24,5],[25,1],[26,6],[27,4],[28,1],[29,6],[30,2],[31,3],[32,4],[33,5],[34,6],[35,6],[36,1],[37,1],[38,2],[39,1],[40,6],[41,1],[42,6],[43,2],[44,6],[45,2],[46,2],[47,2],[48,11],[49,5],[50,5],[51,4],[52,6],[53,5],[54,1],[55,1],[56,2],[57,4],[58,3],[59,6],[60,5]
]
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
from tabulate import tabulate

table = pd.DataFrame(recipe_rows, columns=recipe_headers)

# Since 4 is small sample size, i took 10 to make central limit theorem more apparent

def calculate(table):

    mean = table['X'].mean()
    st_dev = table['X'].std()
    return mean,st_dev

def get_samples(tables,size):

    samples = [table['X'].sample(n=size) for i in range(10)]
    # for i in range(1,10):
    #     print("Sample :" + str(i))
    #     print (samples[i])
    return samples


def get_mean_sample(samples):
    mean_list = []
    all_samples = []
    # List for mean values of samples
    for i in range(10):
        mean = round(samples[i].mean(),1)
        mean_list.append(mean)
        all_samples.extend(samples[i])
    print("Mean of all Samples combined for size ", len(samples[0]), ": ", float(statistics.mean(mean_list)))
    print ("St Dev of all samples combined for size ", len(samples[0]), ": ",  statistics.stdev(all_samples))

    return mean_list


def get_histograph(population,n = 0):

    if n == 0:

        plt.hist(population["X"], bins=range(1, 13), align="left", rwidth=0.8)
        plt.xticks(range(1, 13))
        plt.xlabel("Days")
        plt.ylabel("Frequency")
        plt.title("Histogram for original population")

        plt.show()
    else:
        if n == 5:
            mean_list = mean_list_5
        elif n ==10 :
            mean_list = mean_list_10
        step = 0.5
        start = int(min(mean_list))
        stop = max(mean_list) + 2
        bin_edges = np.arange(start, stop, step=step)

        plt.hist(mean_list, bins=bin_edges,color='crimson', ec='white', rwidth= 0.8)
        plt.plot( color='black',  linewidth=2)
        plt.xticks(bin_edges,fontsize=16)
        plt.yticks(np.arange(0, int(max(np.histogram(mean_list, bins=bin_edges)[0]))+2, 1),fontsize=16)
        plt.tight_layout()
        plt.xlabel("Days",fontsize=16)
        plt.ylabel("Frequency",fontsize=16)
        plt.title("Histogram for sample with size  "+ str(n),fontsize=16)
        plt.show()





if __name__ == '__main__':
    # Task 1
    mean, st_dev = calculate(table)
    print("μx = ", mean)
    print("σx = ", st_dev)
    # Collect the Data 1 + 2
    samples_5 = get_samples(table,5)
    mean_list_5 = get_mean_sample(samples_5)

    # Collect the Data 3 + 4
    samples_10 = get_samples(table,10)
    mean_list_10 = get_mean_sample(samples_10)

    # Collect the Data 5
    get_histograph(table)

    # Repeat the Procedure for n = 5
    get_histograph(table,5)

    # Repeat the Procedure for n = 10
    get_histograph(table,10)