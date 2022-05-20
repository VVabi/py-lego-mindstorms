import gc
import micropython
import hub_runtime

import utime
import json
import mindstorms
import time
from communication_helpers import *

def top_level():
    hub_runtime.init(0)
    mshub   = mindstorms.MSHub()
    motor_a = mindstorms.Motor('B')
    motor_a.set_stop_action('hold')
    motor_a.stop()
    motor_a.run_to_position(0, 'clockwise', 50)
    start_ts=time.time_ns()
    for i in range(1000000):
        if not CommunicationHelper.is_connected():
            utime.sleep(0.5)
            continue
        utime.sleep(0.05)
        gyro_data = dict()
        gyro_data["roll"]    = mshub.motion_sensor.get_roll_angle()

        gyro_data["pitch"]   = mshub.motion_sensor.get_pitch_angle()
        gyro_data["yaw"]     = mshub.motion_sensor.get_yaw_angle()
        gyro_data["encoder"] = motor_a.get_position()
        gyro_data["timestamp"] =(time.time_ns()-start_ts)/1000000
        CommunicationHelper.write_dict_to_serial(gyro_data)
        recv = CommunicationHelper.receive_json_from_serial()
    
        if recv is not None:
            motor_a.start(recv["a"])