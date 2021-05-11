import csv
import numpy as np
from matplotlib import pyplot as plt
import enum
import os
from utilities import read_csv_rt, count_lines

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
def data_plotter_rt(filename: str, joint: int, plotsize: int = 0, title: str = '') -> None:
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

    if plotsize != 0:
        commands = commands[0:plotsize]
        feedback = feedback[0:plotsize]
        cycle_list = cycle_list[0:plotsize]

    plt.plot(cycle_list, commands, label='Command')
    plt.plot(cycle_list, feedback, label='Feedback')
    plt.legend(loc='upper right')
    if title == '':
        plt.title('Real-Time Control, Joint: {}'.format(Joints(joint).name))
    else:
        plt.title(title)
    plt.ylabel('Joint velocity [deg/s]')
    plt.xlabel('Cycles')
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

#Plots feedback from multiple csv files as well as command velocity from the first file
def compare_plots(filenames: list, joint: int, 
    cutoff: int = 1500,
    title: str = 'Step Response',
    legend: list = []) -> None:

    feedback_list = []
    command, feedback = read_csv_rt(filenames[0], joint)
    command = command[0:cutoff]
    feedback_list.append(feedback[0:cutoff])
    for i in range(1,len(filenames)):
        _, feedback = read_csv_rt(filenames[i], joint)
        feedback_list.append(feedback[0:cutoff])
    
    i = 0
    while(len(legend) <= len(feedback_list)):
        legend.append('Feedback' + ' ' + str(i))
        i += 1

    cycle_list = np.linspace(0, cutoff, cutoff)
    command = np.rad2deg(command)
    plt.plot(cycle_list, command, label='Command')

    i = 0
    for feedback in feedback_list:
        feedback = np.rad2deg(feedback)
        plt.plot(cycle_list, feedback, label=legend[i])
        i += 1

    plt.legend(loc='upper right')
    plt.title(title + ', Joint: {}'.format(Joints(joint).name))
    plt.ylabel('Joint velocity [deg/s]')
    plt.xlabel('Cycles')
    plt.grid(True)
    plt.show()
    
def plot_all_joints(filename: str):
    fig, ax = plt.subplots(nrows=6, ncols=1)
    ax_nr = 0
    
    for i in range(6):
        commands, feedback = read_csv_rt(filename, i)
        total_lines = count_lines(filename)

        for j in range(len(commands)):
            commands[j] = np.rad2deg(commands[j])
            feedback[j] = np.rad2deg(feedback[j])
            
        cycle_list = np.linspace(0, total_lines, total_lines)
        ax[ax_nr].plot(cycle_list, commands, label='Command')
        ax[ax_nr].plot(cycle_list, feedback, label='Feedback' + str(i))
        ax[ax_nr].legend(loc='upper right')
        if ax_nr == 0:
            ax[ax_nr].set_title('Real time control')
        ax[ax_nr].grid(True)

        ax_nr += 1
    
    plt.show()  

