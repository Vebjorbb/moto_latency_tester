from latency_tester import LatencyTester
from moto.simple_message import ValidFields, JointTrajPtFull
import numpy as np

t = LatencyTester('192.168.255.200')

pos = JointTrajPtFull(
                groupno=0,
                sequence=1,
                valid_fields=ValidFields.TIME | ValidFields.POSITION | ValidFields.VELOCITY,
                time=10,
                pos=np.deg2rad([10.0, 10.0, 10.0, 10.0, 10.0, 0, 0, 0, 0, 0]),
                vel=[0.0]*10,
                acc=[0.0]*10
                )
                