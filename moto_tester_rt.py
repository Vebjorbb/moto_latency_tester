from moto import Moto
import time
import csv
from utilities import count_lines

class MotoTesterRt(Moto):
    def __init__(self, ip, control_group_defs):
        super().__init__(ip, control_group_defs,
        start_motion_connection = False,
        start_state_connection = False,
        start_io_connection = False,
        start_real_time_connection = True
        )

    #Checks the operation frequency of the system
    def check_frequency(self):
        self.rt.start_rt_mode()
        start_time = time.time()
        time.sleep(2)
        self.rt.stop_rt_mode()
        end_time = time.time()
        total_time = end_time - start_time
        
        time.sleep(1)
        lines = count_lines('motion_log_rt.csv')

        print('Total lines: {}\nTotal time: {}\nApproximated frequency: {}'.format(lines, total_time, lines/total_time))
