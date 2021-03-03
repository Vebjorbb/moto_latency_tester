from latency_tester import LatencyTester
from moto.simple_message import ValidFields, JointTrajPtFull
from moto import ControlGroupDefinition
import numpy as np

t = LatencyTester('192.168.255.200', [
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

pos = JointTrajPtFull(
                groupno=0,
                sequence=1,
                valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
                time=10,
                pos=np.deg2rad([10.0, 10.0, 10.0, 10.0, 10.0, 0, 0, 0, 0, 0]),
                vel=[0.0]*10,
                acc=[0.0]*10
                )
                