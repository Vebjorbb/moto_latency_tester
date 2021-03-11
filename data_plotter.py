import csv
import numpy as np
from matplotlib import pyplot as plt
import enum
import os

class Joints(enum.Enum):
    S = 0
    L = 1
    U = 2
    R = 3
    B = 4
    T = 5

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

    for i in range(len(commands)):
        commands[i] = np.rad2deg(commands[i])
        feedback[i] = np.rad2deg(feedback[i])
        
    cycle_list = np.linspace(0, total_lines, total_lines)
    plt.plot(cycle_list, commands, label='Command')
    plt.plot(cycle_list, feedback, label='Feedback')
    plt.legend(loc='upper right')
    plt.title('Real-Time Control, Joint: {}'.format(Joints(joint).name))
    plt.grid(True)
    plt.show()


#Plots all files in a directory
def data_multiplotter_rt(directory: str, joint: int) -> None:
    nr_of_files = 0
    for file in os.listdir(directory):
        if os.path.isfile((os.path.join(directory,file))):
            nr_of_files +=1
    
    fig, ax = plt.subplots(nrows=nr_of_files, ncols=1)
    ax_nr = 0
    
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory,file)):
            commands = []
            feedback = []
            total_lines = 0
            with open(os.path.join(directory, file)) as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    line = line[0].split('\t')
                    commands.append(float(line[joint+10]))
                    feedback.append(float(line[joint]))
                    total_lines = csv_reader.line_num

            for i in range(len(commands)):
                commands[i] = np.rad2deg(commands[i])
                feedback[i] = np.rad2deg(feedback[i])
            
            cycle_list = np.linspace(0, total_lines, total_lines)
            ax[ax_nr].plot(cycle_list, commands, label='Command')
            ax[ax_nr].plot(cycle_list, feedback, label='Feedback')
            ax[ax_nr].legend(loc='upper right')
            if ax_nr == 0:
                ax[ax_nr].set_title('Joint: {}'.format(Joints(joint).name))
            ax[ax_nr].grid(True)

            ax_nr += 1
    
    plt.show()  
    