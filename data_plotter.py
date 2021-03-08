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
        for i  in range(100, 1100):
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

        
print(calculate_latency('motion_log_rt_ex_fixed.csv'))