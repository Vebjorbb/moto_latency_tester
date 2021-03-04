from moto_tester_rt import MotoTesterRt
from moto import ControlGroupDefinition
from moto_tester import MotoTester

rt = MotoTesterRt('192.168.255.200', [
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

