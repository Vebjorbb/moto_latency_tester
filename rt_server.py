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
    #server = start_udp_server(("localhost", 50244))
    started = False

    t0 = time.time()    
    p0 = None

    #Parameters for PID-controller
    total_error = 0
    curr_vel = 0
    prev_vel = 0
    curr_pos = 0
    prev_pos = 0 
    k_p = 0
    k_i = 0
    k_d = 0
    while True:

        try:
            bytes_, addr = server.recvfrom(1024)
            if not bytes_:
                logging.error("Stopping!")
                break

            if not started:
                server.settimeout(1.0)
                started = True


            msg = SimpleMessage.from_bytes(bytes_)
            state: MotoRealTimeMotionJointStateEx = msg.body

            if p0 is None:
                p0 = copy(state.joint_state_data[0].pos)
            
            curr_pos = state.joint_state_data[0].pos[0]

            if curr_pos < prev_pos:
                state.joint_state_data[0].vel[0] = -state.joint_state_data[0].vel[0]

            prev_pos = curr_pos

            print("state:   {}".format(state.joint_state_data[0].vel[0]))
        
            # pd = np.deg2rad(10)
            # Kv = 0.1
            # vd = Kv * (pd - state.joint_state_data[1].pos[0])
            vd  = 0.3 * (np.sin(3.0 * time.time() - t0))
            # vd  = 0.05 * (np.sin(0.1 * time.time() - t0))

            #vd = 0.05


            print("command: {}".format(vd))

            #Calculate variables for PID-controller
            curr_vel = state.joint_state_data[0].vel[0]
            error = vd - state.joint_state_data[0].vel[0]
            total_error = total_error + error
            
            print("error: {}".format(error))

            #Adjust velocity with PID-controller
            vd_corr = vd + k_p*error + k_i*total_error + k_d*(curr_vel-prev_vel)
            prev_vel = curr_vel

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
                            0, [vd_corr, 0.0, 0.0, 0.0, 0.0, 0.0]
                        ),
                        MotoRealTimeMotionJointCommandExData(1, [0, 0]),
                        
                    ],
                ),
            )

            server.sendto(command_msg.to_bytes(), addr)
            #csv_writer.writerow(state.joint_state_data[1].vel + command_msg.body.joint_command_data[1].command + state.joint_state_data[1].pos)
            #csv_writer.writerow(state.joint_state_data[0].vel + command_msg.body.joint_command_data[0].command + state.joint_state_data[0].pos)
            csv_writer.writerow(state.joint_state_data[0].vel + [vd]*10 + state.joint_state_data[0].pos)

        except socket.timeout as e:
            logging.error("Timed out!")
            break


if __name__ == "__main__":

    main()