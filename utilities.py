from moto.simple_message import JointTrajPtFull, ValidFields
from typing import List
import numpy as np
import csv
import os
from matplotlib import pyplot as plt

#Generates trajectory points from a position and time argument
def make_traj_pt(pos: List[float], 
                time: int,
                groupno = 0,
                sequence= 1,
                valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
                vel = [0.0]*10,
                acc = [0.0]*10
                ) -> JointTrajPtFull:
    for _ in range(4):
        pos.append(0.0)
    point = JointTrajPtFull(groupno, sequence, valid_fields, time, np.deg2rad(pos), vel, acc)
    return(point)


#Changes the velocity sign correctly
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

#Changes the velocity sign for all files in a directory
def fix_vel_multi(directory: str) -> None:
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            fix_velocity_sign(os.path.join(directory, file))


def calculate_lag(filename:str, joint: int):
    commands = []
    feedbacks = []

    #Reads data from csv-file and saves it in lists
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = line[0].split('\t')
            for element in line:
                float(element)
            commands.append(line[10:20])
            feedbacks.append(line[0:10])
    
    #Convert from lists of strings to lits of floats
    for command in commands:
        for i in range(len(command)):
            command[i] = float(command[i])
    
    for feedback in feedbacks:
        for i in range(len(feedback)):
            feedback[i] = float(feedback[i])
    
    cycle = 100
    current_command = commands[cycle][joint]
    previous_command = commands [cycle - 1][joint]
    
    while np.sign(previous_command) == np.sign(current_command):
        cycle += 1
        current_command = commands[cycle][joint]
        previous_command = commands[cycle-1][joint]

    lag = 0
    current_feedback = feedbacks [cycle][joint]
    previous_feedback = feedbacks[cycle - 1][joint]

    while np.sign(previous_feedback) == np.sign(current_feedback):
        lag += 1
        current_feedback = feedbacks[cycle + lag][joint]
        previous_feedback = feedbacks[cycle + lag - 1][joint]

    return(lag)


def calculate_lag_multi(directory: str, joint: int):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            print(calculate_lag(os.path.join(directory, file), joint))   
            