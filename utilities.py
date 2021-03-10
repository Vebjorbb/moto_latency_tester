from moto.simple_message import JointTrajPtFull, ValidFields
from typing import List
import numpy as np
import csv
import os

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

#Calculates the latency for each joint from a rt test-file
def calculate_latency(filename: str):
    latencies = [0.0]*10
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

    #An average latency is calculated for each joint
    for joint in range(len(latencies)):
        latency_list = []
        for i  in range(100, 2100):
            current_command = commands[i][joint]
            previous_command = commands[i-1][joint]

            #Checks if the command velocity is increasing or decreasing
            rising_command = 0
            if current_command > previous_command:
                rising_command = 1
            else:
                rising_command = 0


            current_feedback = 0
            previous_feedback = 0
            rising_feedback = 0

            latency_counter = 0 
            
            for j in range(i, len(feedbacks)):
                current_feedback = feedbacks[j][joint]
                previous_feedback = feedbacks[j-1][joint]
                
                #Checks if the feedback-velocity is increasing or decreasing
                if current_feedback > previous_feedback:
                    rising_feedback = 1
                else:
                    rising_feedback = 0

                #Compares feedback signal to command signal to determine latency
                if current_command > previous_feedback and current_command < current_feedback and rising_feedback == rising_command:
                    latency_list.append(latency_counter)
                    break
                elif current_command < previous_feedback and current_command > current_feedback and rising_feedback == rising_command:
                    latency_list.append(latency_counter)
                    break
                elif current_command == current_feedback:
                    latency_list.append(latency_counter)
                    break
                else:
                    latency_counter += 1
            
        #Calculate average latency and save it in a list    
        latencies[joint] = sum(latency_list)/len(latency_list)
    
    return(latencies)

#Calculates latency for all files in a directory
def multiple_latency(directory: str) -> None:
    latency_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory,file)):
            latency = calculate_latency(os.path.join(directory, file))
            latency_list.append(latency)
            print('{}\n{}\n'.format(file, latency))
    return(latency_list)


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

#Calculates the average latency of all files in a directory
def calc_average_latency(directory: str):
    latency_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.joint(directory, file)):
            latency_list.append(calculate_latency(os.path.join(directory, file)))

    avg_latency = [0.0]*10
    for latency in latency_list:
        counter = 0
        for element in latency:
            avg_latency[counter] +=element
            counter += 1

    for i in range(len(avg_latency)):
        avg_latency[i] = avg_latency[i]/len(latency_list)

    return(avg_latency)