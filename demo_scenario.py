# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:48:22 2021

@author: m01winke
"""

from modules.pythonic_function_server import PythonicFunctionServer
from modules.connection.scene_suite_connection import SceneSuiteConnection
from modules.response.scene_suite_response import SceneSuiteResponse

from demo_vehicle import DemoVehicle


class DemoScenario:
    def __init__(self, metadata):
        self.metadata = metadata
        
        # actors are defined here
        self.demo_vehicle = DemoVehicle()

    def process_frame(self, sensordata, frame_id):
        
        response = SceneSuiteResponse()
        response["chn.ego"] = self.demo_vehicle.process_frame(sensordata["simple"], sensordata["objects"], frame_id)

        return response.as_xml()


if __name__ == "__main__":

    connection = SceneSuiteConnection(port=4321)
    pfs = PythonicFunctionServer(connection)
    pfs.run(DemoScenario)
