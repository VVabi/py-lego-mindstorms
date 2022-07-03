import gc
import micropython
import hub_runtime

import utime
import json
import mindstorms
import time
from communication_helpers import *


class Motors:
    def __init__(self):
        self.motors = dict()

    
    def handle_register_motor(self, config):
        port = config["port"]
        self.motors[port] = mindstorms.Motor(port)
    
    def handle_set_pwm(self, pwm_msg):
        self.motors[pwm_msg["port"]].start(pwm_msg["pwm"])


def top_level():
    hub_runtime.init(0)
    handler_map = dict()
    motors = Motors()
    
    handler_map["motor/register"] = motors.handle_register_motor
    handler_map["motor/set_pwm"]  = motors.handle_set_pwm

    mshub   = mindstorms.MSHub()
    
    start_ts=time.time_ns()
    while True:
        if not CommunicationHelper.is_connected():
            utime.sleep(0.5)
            continue
        utime.sleep(0.05)
        gyro_data = dict()
        gyro_data["roll"]    = mshub.motion_sensor.get_roll_angle()

        gyro_data["pitch"]   = mshub.motion_sensor.get_pitch_angle()
        gyro_data["yaw"]     = mshub.motion_sensor.get_yaw_angle()
        #gyro_data["encoder"] = motor_a.get_position()
        gyro_data["timestamp"] =(time.time_ns()-start_ts)/1000000
        sensor_msg = {}
        sensor_msg["topic"] = "sensor"
        sensor_msg["payload"] = gyro_data
        CommunicationHelper.write_dict_to_serial(sensor_msg)
        recv = CommunicationHelper.receive_json_from_serial()
        
        if recv is not None:
            handler_map[recv["topic"]](recv["payload"])