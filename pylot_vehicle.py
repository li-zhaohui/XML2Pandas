# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:41:52 2021

@author: m01winke
"""

import numpy as np
import joblib
from pathlib import Path
import pandas as pd

import xml.etree.ElementTree as ET

from modules.object.vehicle import Vehicle
from modules.object.pylot_agent.pylot_2d_agent import Pylot2DAgent
from modules import utils


def get_waypoints_from_carla_route(xml_file, route_id="0"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    waypoints = []
    
    for route in root.iter("route"):
        if route.attrib["id"] == route_id:
            for waypoint in route.iter("waypoint"):
                
                waypoints.append({"x": float(waypoint.attrib["x"]),
                                  "y": float(waypoint.attrib["y"]),
                                  "z": float(waypoint.attrib["z"]),
                                  "roll": float(waypoint.attrib["roll"]),
                                  "pitch": float(waypoint.attrib["pitch"]),
                                  "yaw": float(waypoint.attrib["yaw"]),
                                  })
                
    waypoints = pd.DataFrame.from_records(waypoints)
    return waypoints


def apply_noise_to_sensordata(sensordata, mu=0, sigma=0.2):
    noise = np.random.normal(mu, sigma, [len(sensordata), 3])
    noisy_sensordata = sensordata.copy()
    noisy_sensordata[["x", "y", "z"]] += noise
    
    return noisy_sensordata


def get_pose(egodata):
    pos_x = float(egodata.loc[egodata["type"] == "Pos", "x"])
    pos_y = float(egodata.loc[egodata["type"] == "Pos", "y"])
    veloc_x = float(egodata.loc[egodata["type"] == "Veloc", "x"])
    veloc_y = float(egodata.loc[egodata["type"] == "Veloc", "y"])
    yaw = float(egodata.loc[egodata["type"] == "AngleZ", "value"])
    pose = {"x": pos_x, "y": pos_y, "vx": veloc_x, "vy": veloc_y, "yaw": yaw}
    
    return pose


def get_linear_speed(egodata):
    return float(egodata.loc[egodata["type"] == "Veloc", "x"])


def get_ground_objects(sensordata):
    ground_objects = {"hero_vehicle":{"id":"mov.Ego"},
                      "vehicles":{},
                      "walkers":{},
                      "traffic_lights":{},
                      "stop_signs":{},
                      "speed_limits":{},
                      "static_obstacles":{},
                      }
    
    if len(sensordata) > 0:
        for movement_id in sensordata["movementId"].unique():
            object_data = sensordata[sensordata["movementId"] == movement_id]
            person_dict = {"x": object_data["x"].min(), "y": object_data["y"].min(), "z": object_data["z"].min()}
            
        ground_objects["walkers"][movement_id] = person_dict
    
    return ground_objects


class PylotVehicle(Vehicle):
    def __init__(self):
        super().__init__()
        
        # init pylot modules here
        self._pylot_2d_agent = Pylot2DAgent()
        self._pylot_2d_agent.setup("/home/m01winke/Documents/pythonic-function-server/modules/object/pylot_agent/single_scenarios.conf")
        
        # self._waypoints = joblib.load("/home/m01winke/Documents/pythonic-function-server/modules/object/pylot_agent/waypoints.joblib")
        self._waypoints = get_waypoints_from_carla_route('/home/m01winke/Documents/2103_pylot/scenario_runner/srunner/data/routes_single_scenarios.xml')
        self._opendrive = Path("/home/m01winke/Documents/2103_pylot/pylot/dependencies/CARLA_0.9.10.1/CarlaUE4/Content/Carla/Maps/OpenDrive/Town01.xodr").read_text()
        
    def destroy(self):
        self._pylot_2d_agent.destroy()
        
    def process_frame(self, egodata, sensordata, frame_id):
        
        # sensordata.plot.scatter(x="x", y="y")
        
        # # apply noise to data (varies across concrete scenarios)
        # noisy_sensordata = apply_noise_to_sensordata(sensordata)
        # noisy_sensordata.plot.scatter(x="x", y="y")
        
        # parse data for pylot
        simulation_time = frame_id * 0.05
        input_data = {}
        input_data["pose"] = get_pose(egodata)
        input_data["ground_objects"] = get_ground_objects(sensordata)
        
        # send data to pylot and get response
        if frame_id == 1:
            output_control = self._pylot_2d_agent.run_step(input_data, simulation_time, self._opendrive, self._waypoints)
        else:
            output_control = self._pylot_2d_agent.run_step(input_data, simulation_time)
        
        # parse response (acceleration and steering?)
        response = {}
        response["Acceleration"] = 3.0 * output_control.throttle - np.sign(get_linear_speed(egodata)) * 9.0 * output_control.brake
        response["YawRadius"] = 5.0 / output_control.steer
        
        # apply vehicle dynamics (varies across concrete scenarios)
        # PT2?
        
        return response
    
    
if __name__ == "__main__":
    vehicle = PylotVehicle()