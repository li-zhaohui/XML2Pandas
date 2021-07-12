# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:48:22 2021

@author: m01winke
"""

import pandas as pd

class PythonicFunctionServer:
    global_metadata = pd.DataFrame()
    global_sensordata = pd.DataFrame()

    def __init__(self, connection):
        
        # connection to the (simulation) environment, e.g. IAV Scene Suite
        self._connection = connection
        self._scenario = None
        self._frame_id = 0

        self.global_metadata = pd.DataFrame()
        self.global_sensordata = pd.DataFrame()

    def _process_scenario(self, scenario):
        
        print("INFO: Waiting for connection at {}.".format(self._connection.where))
        self._connection.listen()
        
        self._frame_id = 0
        while True:
            
            if self._frame_id == 0:
                # initialize scenario
                stream_is_open, metadata, sensordata = self._connection.receive_metadata_sensordata()
                self.global_metadata.append(metadata)
                self.global_metadata.append(sensordata)

                if not stream_is_open:
                    print("ERROR: Could not receive first frame.")
                    break
                self._scenario = scenario(metadata)
            else:
                stream_is_open, sensordata = self._connection.receive_sensordata()
                self.global_metadata.append(sensordata)
                if not stream_is_open:
                    break

            self._frame_id += 1
            print("DEBUG: Processing frame {}".format(self._frame_id))

            # process frame
            response = self._scenario.process_frame(sensordata, self._frame_id)

            self._connection.send_response(response)

        print(self.global_metadata)
        print(self.sensordata)
        
        self._connection.close()

    def run(self, scenario):
        """
        This function will keep the server running to process multiple simulations.

        In the usual setting, Scene Suite processes one or more databases containing
        a number of scenarios.

        Returns
        -------
        None.

        """
        while True:
            self._process_scenario(scenario)
