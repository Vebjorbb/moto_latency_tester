from moto import Moto, ControlGroupDefinition
from moto.simple_message import JointTrajPtFull, ValidFields, ReplyType, ResultType
import numpy as np
import csv
import time

class MotoTester(Moto):
    def __init__(self, ip, control_group_defs):
        super().__init__(ip, control_group_defs)
        while self.state.joint_feedback(0) == None:
            pass
        self.p0 = JointTrajPtFull(
            groupno=0,
            sequence=0,
            valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
            time=0,
            pos = self.state.joint_feedback(0).pos,
            vel = self.state.joint_feedback(0).vel,
            acc=self.state.joint_feedback(0).acc
        )
        
    #Updates the current position and sets sequence and time to 0
    def update_p0(self) -> None:
        self.p0 = JointTrajPtFull(
            groupno=0,
            sequence=0,
            valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
            time=0,
            pos = self.state.joint_feedback(0).pos,
            # vel = self.m.state.joint_feedback(0).vel,
            vel = [0.0]*10,
            acc=self.state.joint_feedback(0).acc
        )

    #Moves the robot to home position over 10 seconds
    def move_to_home(self) ->None:
        if self.motion.check_motion_ready().body.result == ResultType.FAILURE:
            print('Robot not ready for motion')
        elif self.motion.check_motion_ready().body.result == ResultType.SUCCESS:
            self.update_p0()
            home = JointTrajPtFull(
                groupno=0,
                sequence=1,
                valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
                time=10,
                pos=[0.0]*10,
                vel=[0.0]*10,
                acc=[0.0]*10
                )
            self.motion.send_joint_trajectory_point(self.p0)
            self.motion.send_joint_trajectory_point(home)
    
    #Disconnects the Moto object and quits python
    def quit(self):
        self.motion.disconnect()
        quit()


    #slowly moves the robot to an example position
    def move_to_pos(self, pos: JointTrajPtFull) -> None:
        if self.motion.check_motion_ready().body.result == ResultType.FAILURE:
            print('Robot not ready for motion')
        elif self.motion.check_motion_ready().body.result == ResultType.SUCCESS:
            self.update_p0()
            self.motion.send_joint_trajectory_point(self.p0)
            self.motion.send_joint_trajectory_point(pos)

    #Logs the joint positions of the robot while moving from one position to another  
    def logger(self, pos: JointTrajPtFull, log_freq = 250, buffer = 0.5) -> None:

        cycle_counter = 0

        with open('motion_log.csv', 'w') as new_file:
            print('Logging...')
            csv_writer = csv.writer(new_file, delimiter='\t')

            cycle_counter = 0
            while cycle_counter < log_freq*buffer:
                csv_writer.writerow(self.state.joint_feedback(0).pos)
                cycle_counter += 1
                time.sleep(1/log_freq)

            self.move_to_pos(pos)
            cycle_counter = 0
            while cycle_counter < log_freq*pos.time:
                csv_writer.writerow(self.state.joint_feedback(0).pos)
                cycle_counter += 1
                time.sleep(1/log_freq)

            cycle_counter = 0
            while cycle_counter < log_freq*buffer:
                csv_writer.writerow(self.state.joint_feedback(0).pos)
                cycle_counter += 1
                time.sleep(1/log_freq)

            print('Finished logging!')
    
