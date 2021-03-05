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
    total_lines = 0

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for line in csv_reader:
            line = line[0].split('\t')
            commands.append(float(line[joint+10]))
            feedback.append(float(line[joint]))

            total_lines = csv_reader.line_num

    cycle_list = np.linspace(0, total_lines, total_lines)
    plt.plot(cycle_list, commands, label='Command')
    plt.plot(cycle_list, feedback, label='Feedback')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

def fix_velocity_sign(filename: str) -> None:
    name_components = filename.split('.')
    new_filename = name_components[0] + '_fixed.' + name_components[1]

    current_pos = [0.0]*10
    previous_pos = [0.0]*10

    with open(filename, 'r') as raw_data:
        csv_reader =csv.reader(raw_data)
        with open(new_filename, 'w') as fixed_data:
            csv_writer = csv.writer(fixed_data, delimiter='\t')
            for line in csv_reader:
                line = line [0].split('\t')
                current_pos = line[20:29]
                for i in range(len(current_pos)):
                    if float(current_pos[i]) < float(previous_pos[i]):
                        line[i] = "-" + line[i]
                csv_writer.writerow(line)
                previous_pos = current_pos   

    