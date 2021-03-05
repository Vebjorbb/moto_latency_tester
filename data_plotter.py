import csv
import numpy as np
from matplotlib import pyplot as plt

#Plots data from motion_log.csv
def data_plotter(filename: str, joint: int, total_time: int) -> None:
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = line[0].split('\t')
            data.append(line[joint])
    for i in range(len(data)):
        data[i] = np.rad2deg(float(data[i]))
    time_list = np.linspace(0,total_time, len(data))

    plt.plot(time_list, data)
    plt.show()

#Plots data from motion_log_rt.csv
def data_plotter_rt(filename: str, joint: int) -> None:
    commands = []
    feedback = []
    current_pos = 0
    previous_pos = 0
    total_lines = 0

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for line in csv_reader:
            line = line[0].split('\t')
            current_pos = float(line[joint+20])
            commands.append(float(line[joint+10]))

            if current_pos < previous_pos:
                feedback.append(-float(line[joint]))
            else:
                feedback.append(float(line[joint]))
            
            previous_pos = current_pos

            total_lines = csv_reader.line_num

    cycle_list = np.linspace(0, total_lines, total_lines)
    plt.plot(cycle_list, commands, label='Command')
    plt.plot(cycle_list, feedback, label='Feedback')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()
    