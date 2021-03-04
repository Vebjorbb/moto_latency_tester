from moto_tester import MotoTester
from moto.simple_message import ValidFields, JointTrajPtFull
from moto import ControlGroupDefinition
import numpy as np
from utilities import make_traj_pt

t = MotoTester('192.168.255.200', [
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
    ]
    )

pos = make_traj_pt([20.0]*6, 1)