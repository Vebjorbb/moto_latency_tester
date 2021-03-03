import csv
import numpy as np
from matplotlib import pyplot as plt

def data_plotter(filename: str, joint: int, total_time: int) -> None:
    
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = line[0].split('\t')
            data.append(line[joint])

    time_list = np.linspace(0,total_time, len(data))

    plt.plot(time_list, data)
    plt.show()       

data_plotter('motion_log.csv', 0, 1)