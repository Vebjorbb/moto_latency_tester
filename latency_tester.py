from moto import Moto, ControlGroupDefinition
from moto.simple_message import JointTrajPtFull, ValidFields, ReplyType, ResultType
import numpy as np
import csv
import time

class LatencyTester():
    def __init__(self, ip: str):
        self.m = Moto(
            ip,
            [
                ControlGroupDefinition(
                    groupid="R1",
                    groupno=0,
                    num_joints=6,
                    joint_names=[
                        "joint_1_s",
                        "joint_2_l",
                        "joint_3_u",
                        "joint_4_r",
                        "joint_5_b",
                        "joint_6_t",
                    ],
                ),
            ],
        )
        while self.m.state.joint_feedback(0) == None:
            pass
        self.p0 = JointTrajPtFull(
            groupno=0,
            sequence=0,
            valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
            time=0,
            pos = self.m.state.joint_feedback(0).pos,
            vel = self.m.state.joint_feedback(0).vel,
            acc=self.m.state.joint_feedback(0).acc
        )
        
    #Updates the current position and sets sequence and time to 0
    def update_p0(self) -> None:
        self.p0 = JointTrajPtFull(
            groupno=0,
            sequence=0,
            valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
            time=0,
            pos = self.m.state.joint_feedback(0).pos,
            # vel = self.m.state.joint_feedback(0).vel,
            vel = [0.0]*10,
            acc=self.m.state.joint_feedback(0).acc
        )

    #Moves the robot to home position over 10 seconds
    def move_to_home(self) ->None:
        if self.m.motion.check_motion_ready().body.result == ResultType.FAILURE:
            print('Robot not ready for motion')
        elif self.m.motion.check_motion_ready().body.result == ResultType.SUCCESS:
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
            self.m.motion.send_joint_trajectory_point(self.p0)
            self.m.motion.send_joint_trajectory_point(home)
    
    #Disconnects the Moto object and quits python
    def quit(self):
        self.m.motion.disconnect()
        quit()


    #slowly moves the robot to an example position
    def move_to_pos(self):
        if self.m.motion.check_motion_ready().body.result == ResultType.FAILURE:
            print('Robot not ready for motion')
        elif self.m.motion.check_motion_ready().body.result == ResultType.SUCCESS:
            self.update_p0()
            pos = JointTrajPtFull(
                groupno=0,
                sequence=1,
                valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
                time=10,
                pos=np.deg2rad([10.0, 10.0, 10.0, 10.0, 10.0, 0, 0, 0, 0, 0]),
                vel=[0.0]*10,
                acc=[0.0]*10
                )
            self.m.motion.send_joint_trajectory_point(self.p0)
            self.m.motion.send_joint_trajectory_point(pos)
            # time.sleep(time)
            # self.m.motion.stop_trajectory_mode()

    #Logs the joint positions of the robot while moving from on position to another  
    def logger(self):
        self.move_to_pos()
        with open('motion_log.csv', 'w') as new_file:
            print('logging')
            csv_writer = csv.writer(new_file, delimiter='\t')

            cycle_counter = 0

            while cycle_counter < 40:
                csv_writer.writerow(self.m.state.joint_feedback(0).pos)
                cycle_counter += 1
                time.sleep(10/40)
    

            




