from moto import Moto

class MotoTesterRt(Moto):
    def __init__(self, ip, control_group_defs):
        super().__init__(ip, control_group_defs,
        start_motion_connection = False,
        start_state_connection = False,
        start_io_connection = False,
        start_real_time_connection = True
        )