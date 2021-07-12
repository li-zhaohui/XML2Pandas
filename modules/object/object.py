# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:58:28 2021

@author: m01winke
"""

class Object:
    def __init__(self):
        self.position = []
        self.orientation = None
        self.velocity = []
        self.acceleration = []
    
    def process_frame(self, xml_dict, frame_id):
        raise("Not implemented.")