# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 14:54:15 2021

@author: m01winke
"""

import pandas as pd
import socket
import xml.etree.ElementTree as ET

from modules.utils import XmlDictConfig


def parse_metadata(xml_tree):

    xml_tree = xml_tree.find("{sop.iav.com}MetaData").attrib

    metadata = {
        "external": [str(xml_tree["external"])],
        "NumOfFrames": [int(xml_tree["NumOfFrames"])],
        "NumOfMovements": [int(xml_tree["NumOfMovements"])],
        "SceneId": [str(xml_tree["SceneId"])],
        "TimeResolution": [float(xml_tree["TimeResolution"])]
    }

    metadata = pd.DataFrame(metadata)
    return metadata


def parse_types(data):
    for key, value in data.items():
        if key in ["x", "y", "z", "time"]:
            data[key] = float(value)
        elif key in ["trackId"]:
            data[key] = int(value)
    
    return data


def parse_sensordata(xml_tree):
    object_list_dataframe = pd.DataFrame()
    simple_sensor_dataframe = pd.DataFrame()

    for frame in xml_tree.findall("{sop.iav.com}Frame"):

        frame_type = frame.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"]
        print(frame_type)
        if frame_type == "SimpleSensorFrame":
            for dynamic_point in frame.findall("{sop.iav.com}DynamicPoint"):
                for determinable_value in dynamic_point.findall("{sop.iav.com}DeterminableValue"):
                    
                    determinable_value_type = determinable_value.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
                    
                    for coordinates in determinable_value.findall("{sop.iav.com}Coordinates"):
                        
                        if determinable_value_type in ["FunctionValue"]:
                            determinable_value_name = determinable_value.attrib["name"]
                            data = {**frame.attrib, **{"type": determinable_value_type}, **{"name": determinable_value_name}, **coordinates.attrib}
                        elif determinable_value_type in ["Pos", "Veloc", "Accel", "YawRate", "AngleX", "AngleY", "AngleZ", "RadialVelocity"]:
                            data = {**frame.attrib, **{"type": determinable_value_type}, **coordinates.attrib}
                        else:
                            print("ERROR: unknown determinable_value type")

                        data = parse_types(data)
                        
                        simple_sensor_dataframe = simple_sensor_dataframe.append(
                            data, ignore_index=True
                        )

        elif frame_type == "ObjectListSensorFrame":
            for sensed_object in frame.findall("{sop.iav.com}SensedObject"):
                for polygon in sensed_object.findall("{sop.iav.com}Polygon"):
                    for vertex in polygon.findall("{sop.iav.com}Vertex"):
                        for determinable_value in vertex.findall(
                            "{sop.iav.com}DeterminableValue"
                        ):
                            for coordinates in determinable_value.findall(
                                "{sop.iav.com}Coordinates"
                            ):
                                data = {
                                    **coordinates.attrib,
                                    **sensed_object.attrib,
                                }
                                
                                data = parse_types(data)
                                print("Data "+str(data))

                                object_list_dataframe = object_list_dataframe.append(
                                    data, ignore_index=True
                                )
        else:
            print("ERROR: unknown frame type")

    return {"simple": simple_sensor_dataframe, "objects": object_list_dataframe}


class SceneSuiteConnection:
    def __init__(self, port=4321):
        self._port = port
        
    @property
    def where(self):
        return "port " + str(self._port)

    def _receive_as_byte_stream(self):
        # receive an initial message of length <= 2^16
        byte_stream = self._connection.recv(65536)

        stream_is_open = True
        if byte_stream:
            # in case the message is longer than 2^16, get the rest of the message
            while not byte_stream.endswith(b"</NetworkData>\n"):
                byte_stream += self._connection.recv(65536)
        else:
            stream_is_open = False

        return stream_is_open, byte_stream
    
    def _receive_as_xml_tree(self):
        stream_is_open, byte_stream = self._receive_as_byte_stream()
        xml_tree = None
        if stream_is_open:
            xml_tree = ET.fromstring(byte_stream)
        return stream_is_open, xml_tree
    
    def listen(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("", self._port))
        self._socket.listen()
        self._connection, _ = self._socket.accept()

    def close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def receive_as_string(self):
        stream_is_open, byte_stream = self._receive_as_byte_stream()
        if stream_is_open:
            string = byte_stream.decode()
        else:
            string = None
        return stream_is_open, string

    def receive_metadata_sensordata(self):
        stream_is_open, xml_tree = self._receive_as_xml_tree()
        if stream_is_open:
            metadata = parse_metadata(xml_tree)
            sensordata = parse_sensordata(xml_tree)
            print(sensordata["objects"])
        else:
            metadata = None
            sensordata = None
        
        return stream_is_open, metadata, sensordata

    def receive_sensordata(self):
        stream_is_open, xml_tree = self._receive_as_xml_tree()
        
        if stream_is_open:
            sensordata = parse_sensordata(xml_tree)
        else:
            sensordata = None
        
        return stream_is_open, sensordata

    def send_response(self, response):
        byte_response = None
        if response == "":
            print("ERROR: response is empty.")
        elif not (response[-1] == "\n"):
            print("ERROR: response must end with new line.")
        else:
            byte_response = response.encode()

        self._connection.sendall(byte_response)
