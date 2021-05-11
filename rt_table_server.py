from copy import copy
import logging
import socket
import time
import numpy as np
import csv

from moto.simple_message import *

logging.basicConfig(level=logging.DEBUG)


def start_udp_server(address):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    return server


def main():
    logger = open('motion_log_rt.csv', 'w')
    csv_writer = csv.writer(logger, delimiter='\t')
    server = start_udp_server(("192.168.255.3", 50244)) 
    started = False

    t0 = time.time()
    cycle_counter = 0

    #Parameters for PID-controller
    total_error = [0]*10
    curr_vel = [0]*10
    prev_error = [0]*10
    prev_pos = [0]*10
    curr_pos = [0]*10
    #Tuning parameters for each joint
    k_p = [1.72*0.5,    1.69*0.5,   0,          0,          0,          0,          0, 0, 0, 0]
    k_i = [0,           0,          0,          0,          0,          0,          0, 0, 0, 0]
    k_d = [4,           3,          0,          0,          0,          0,          0, 0, 0, 0]

    while True:
        try:
            bytes_, addr = server.recvfrom(1024)
            print(cycle_counter)
            if not bytes_:
                logging.error("Stopping!")
                break

            if not started:
                server.settimeout(1.0)
                started = True


            msg = SimpleMessage.from_bytes(bytes_)
            state: MotoRealTimeMotionJointStateEx = msg.body
            
            curr_pos = state.joint_state_data[1].pos

            for i in range(10):
                if np.greater(prev_pos[i],curr_pos[i]):
                    state.joint_state_data[1].vel[i] = -state.joint_state_data[1].vel[i]

            prev_pos = curr_pos
        
            #Define a joint velocity as a sinus-wave, reset t0 to make velocity start at 0
            if cycle_counter == 0:
                t0 = time.time()
            vds  = 0.3 * (np.sin(3.0 * (time.time() - t0)))

            #Step response
            if (cycle_counter > 125) and (cycle_counter < 875):
                vd = [0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            else:
                vd = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
            
            #Define desired joint velocity for each joint
            vd = [vds, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
            

            #Calculate variables for PID-controller
            curr_vel = state.joint_state_data[1].vel
            error = np.subtract(vd, curr_vel)
            total_error = np.add(total_error, error)

            #Adjust velocity with PID-controller
            v_derivative = np.multiply(k_d, np.subtract(error, prev_error))
            v_integral = np.multiply(k_i, total_error)
            v_proportional = np.multiply(k_p, error)
            vd_corr = np.add(vd, np.add(v_proportional, np.add(v_integral, v_derivative)))
            
            prev_error = error

            command_msg: SimpleMessage = SimpleMessage(
                Header(
                    MsgType.MOTO_REALTIME_MOTION_JOINT_COMMAND_EX,
                    CommType.TOPIC,
                    ReplyType.INVALID,
                ),
                MotoRealTimeMotionJointCommandEx(
                    state.message_id,
                    state.number_of_valid_groups,
                    [
                        MotoRealTimeMotionJointCommandExData(
                            0, [0, 0, 0, 0, 0, 0],
                        ),
                        MotoRealTimeMotionJointCommandExData(1, vd_corr[0:2]),
                        
                    ],
                ),
            )

            server.sendto(command_msg.to_bytes(), addr)
            
            csv_writer.writerow(state.joint_state_data[1].vel + vd + state.joint_state_data[1].pos)
            cycle_counter += 1
        except socket.timeout as e:
            logging.error("Timed out!")
            break

if __name__ == "__main__":

    main()