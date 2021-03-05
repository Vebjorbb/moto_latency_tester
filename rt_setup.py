from moto_tester import MotoTester
from moto_tester_rt import MotoTesterRt
from moto import ControlGroupDefinition
from moto.simple_message import ResultType


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

while True:
    print('Starting setup...')
    t.motion.start_trajectory_mode()
    if t.motion.check_motion_ready().body.result != ResultType.SUCCESS:
        sub_code = t.motion.check_motion_ready().body.subcode
        print(f"Setup failed with code: {sub_code}")
        response = input('Would you like to retry? y/n: ')

        if response == 'y':
            pass
        else:
            t.quit()
    
    if t.motion.check_motion_ready().body.result == ResultType.SUCCESS:
        print('Setup successful')
        exit()
