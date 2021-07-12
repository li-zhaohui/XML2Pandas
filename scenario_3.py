# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:41:32 2021

@author: m01winke
"""

from modules.pythonic_function_server import PythonicFunctionServer
from modules.connection.scene_suite_connection import SceneSuiteConnection
from modules.response.scene_suite_response import SceneSuiteResponse

from pylot_vehicle import PylotVehicle


class Scenario_3:
    def __init__(self, metadata):
        self.metadata = metadata
        
        # actors are defined here
        self.ego = PylotVehicle()
        self.pedestrian = None
        self.vending_machine = None

    def process_frame(self, sensordata, frame_id):
        # let all actors determine their response
        response = SceneSuiteResponse()
        response["chn.ego"] = self.ego.process_frame(sensordata["simple"], sensordata["objects"], frame_id)
        # response["chn.pedestrian"] = self.pedestrian.process_frame(xml_dict, frame_id)
        # response["chn.ego"] = self.vending_machine.process_frame(xml_dict, frame_id)
        
        # assess the behavior (KPI calculation)
        
        # logging

        return response.as_xml()


if __name__ == "__main__":
    
    connection = SceneSuiteConnection(port=4321)
    pfs = PythonicFunctionServer(connection)
    pfs.run(Scenario_3)
