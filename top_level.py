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
        for cmd in pwm_msg["commands"]:
            self.motors[cmd["port"]].start(cmd["pwm"])

    def handle_goto_position(self, position_msg):
        self.motors[position_msg["port"]].run_to_position(position_msg["position"])

def top_level():
    hub_runtime.init(0)
    handler_map = dict()
    motors = Motors()
    
    handler_map["motor/register"]       = motors.handle_register_motor
    handler_map["motor/set_pwm"]        = motors.handle_set_pwm
    handler_map["motor/goto_position"]  = motors.handle_goto_position
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
        gyro_data["encoder"] = 131
        gyro_data["timestamp"] =(time.time_ns()-start_ts)/1000000
        sensor_msg = {}
        sensor_msg["topic"] = "sensor"
        sensor_msg["payload"] = gyro_data
        CommunicationHelper.write_dict_to_serial(sensor_msg)
        recv = CommunicationHelper.receive_json_from_serial()
        
        if recv is not None:
            handler_map[recv["topic"]](recv["payload"])