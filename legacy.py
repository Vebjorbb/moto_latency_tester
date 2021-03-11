import csv
import os

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


#Calculates the average latency of all files in a directory
def calc_average_latency(directory: str):
    latency_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
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