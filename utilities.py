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

#output index where dataset crosses x-axis
def find_zeros(data):
    zeros = []
    cycle = 100
    current_data = data[cycle]
    previous_data = data[cycle-1]
    
    while cycle <= (len(data)-100):
        if np.sign(current_data) != np.sign(previous_data):
            zeros.append(cycle)
        cycle += 1 
        current_data = data[cycle]
        previous_data = data[cycle-1]

    return(zeros)


#calculates latency based on zero-points on the sine-waves
def calculate_latency(filename:str, joint: int):
    commands = []
    feedbacks = []
    latencies = []

    #Reads data from csv-file and saves it in lists
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = line[0].split('\t')
            for element in line:
                float(element)
            commands.append(line[joint+10])
            feedbacks.append(line[joint])
    
    #Convert from lists of strings to lits of floats
    for i in range(len(commands)):
        commands[i] = float(commands[i])
    
    for i in range(len(feedbacks)):
        feedbacks[i] = float(feedbacks[i])

    
    #Find all zeros and calculate latency
    zeros = find_zeros(commands)

    for zero in zeros:
        latency = 0
        current_feedback = feedbacks[zero]
        previous_feedback = feedbacks[zero-1]
        
        while np.sign(current_feedback) == np.sign(previous_feedback):
            latency += 1
            current_feedback = feedbacks[zero + latency]
            previous_feedback = feedbacks[zero + latency - 1]
        latencies.append(latency)

    return(latencies)

#Calculates average latency for a file from zero-points
def calculate_average_latency(filename: str, joint: int):
    latencies = calculate_latency(filename, joint)
    avg = sum(latencies)/len(latencies)
    return(avg)

#Calculates and prints latencies and average latency for all files, and total average
def calculate_latency_multi(directory: str, joint: int):
    latency_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            print(file)
            latencies = calculate_latency(os.path.join(directory, file),joint)
            avg = sum(latencies)/len(latencies)
            latency_list.append(avg)
            print('Latencies: {}\nAverage: {}\n'.format(latencies, avg))
    
    total_avg = sum(latency_list)/len(latency_list)
    print('Total average: {}'.format(total_avg))

#Return the number of lines in a csv file
def count_lines(filename: str):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for _ in csv_reader:
            pass
        return(csv_reader.line_num)

def calculate_response_time(filename:str, joint: int):
    commands = []
    feedbacks = []
    response_time =  0

    #Reads data from csv-file and saves it in lists
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            line = line[0].split('\t')
            for element in line:
                float(element)
            commands.append(line[joint+10])
            feedbacks.append(line[joint])
    
    #Convert from lists of strings to lits of floats
    for i in range(len(commands)):
        commands[i] = float(commands[i])
    
    for i in range(len(feedbacks)):
        feedbacks[i] = float(feedbacks[i])
    
    #Calculate when the step response is sendt
    command_time = 0
    i = 0
    while commands[i] == 0:
        command_time += 1
        i += 1

    #Calculate when the robot starts reacting to the response
    feedback_time = 0
    i = 0
    while feedbacks[i] == 0:
        feedback_time += 1
        i += 1
    
    response_time = feedback_time - command_time
    return(response_time)