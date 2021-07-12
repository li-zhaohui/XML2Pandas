# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:10:12 2021

@author: m01winke
"""

from modules.object.vehicle import Vehicle
from modules import utils


class DemoVehicle(Vehicle):
    def __init__(self):
        super().__init__()
        
    def process_frame(self, egodata, sensordata, frame_id):
        
        if len(sensordata) == 0:
            print("Not detecting anything.")
        else:
            print("Detecting {}.".format(sensordata["objects"]))
        
        response = {}
        
        if frame_id == 42:
            response["Acceleration"] = 3.0
            response["FunctionValue"] = {}
            response["FunctionValue"]["display"] = 42
        
        return response