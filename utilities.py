from moto.simple_message import JointTrajPtFull, ValidFields
from typing import List
import numpy as np
from data_plotter import calculate_latency, fix_velocity_sign

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

def multiple_latency(filename: str, nr_of_files: int) -> None:
    for i in range(nr_of_files):
        print(calculate_latency(filename + '_' + '{}'.format(i+1) + '.csv'))


def fix_vel_multi(filename: str, nr_of_files: int) -> None:
    for i in range(nr_of_files):
        fix_velocity_sign(filename + '_' + '{}'.format(i+1) + '.csv')