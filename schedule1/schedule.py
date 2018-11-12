# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 09:38:35 2018

Schedule preparatin script for ISP course 2018

@author: Rinat Khabibullin
"""

import pandas as pd

class WellConnection:
    """
    set of well's connection data
    WELSPECS and COMPDAT keywords data
    """
    def __init__(self,x=1,y=1,z1=1,z2=1):
        self.x = x
        self.y = y
        self.z1 = z1
        self.z2 = z2
        self.group = "G1"
        self.phase = "OIL"
        self.status = "OPEN"
        self.kh = "1*"
        self.skin = 0
        self.diam = 0.2
        self.cf = "1*"
        self.filttablenum = "1*"
        self.depth = "1*"
        
    def get_WELSPECS(self, name = "P1"):
        """
        return WELLSPECS string
        """
        s = (" " + name + " " + self.group +
             " " + str(self.x) +
             " " + str(self.y) +
             " " + str(self.depth) +
             " " + str(self.phase) + " /" )
        return s

    def get_COMPDAT(self, name = "P1"):
        """
        return COMPDAT string
        """
        s = (" " + name + 
             " 2* " + str(self.z1) +
             " " + str(self.z2) +
             " " + str(self.status) +
             " 2* " + str(self.diam) + 
             " 1* " + str(self.skin) + " /" )
        return s        

class WellParamT:
    """
    store all data for some well at moment t
    WCONPROD 
    WCONINJE
    """
    def __init__(self, name):
        self.conn1 = WellConnection()
        self.conn = []
        self.conn.append(self.conn1)
        self.status = "OPEN"
        self.control = "BHP"
        self.lrat = 100
        self.bhp = 50 
        self.name = name
    
    def get_WCONPROD():
        s = " "
        return s
    
    def get_WCONINJE():
        s = " "
        return s
    
    
class Schedule:
    pass
    
    
w1 = WellParamT()
w1.conn[0].x = 3


print("hello "+str(w1.conn[0].get_COMPDAT("I1")))