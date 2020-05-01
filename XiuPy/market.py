# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:05 2020

@author: xiubote
"""

import numpy as np
from XiuPy.share import XiuPyEnvBase, Environment, EventEngine
from XiuPy.datafeed import Datafeed_sql, Datafeed_baostock, Datafeed_wind, Datafeed_dataframe



class BacktestFinished(Exception):
    pass

class BarData(object):

    def __init__(self, datetime, open_price, high_price, low_price, close_price, volume):
        self.datetime = datetime
        self.open = open_price
        self.high = high_price
        self.low = low_price
        self.close = close_price
        self.volume = volume

    def __str__(self):
        return f"{self.datetime} {self.open} {self.high} {self.low} {self.close}"

class Market(XiuPyEnvBase):

    def __init__(self, security, size=500):

        self.count = 0
        self.size = size
        self.inited= False
        self.security = security
        self.open_array = np.zeros(size)
        self.high_array = np.zeros(size)
        self.low_array = np.zeros(size)
        self.close_array = np.zeros(size)
        self.volume_array = np.zeros(size)
        self.columns = self.env.datafeed[self.security].columns
        self.type = 'Market'

    def update_bar(self):
        try:

            bar = self.env.datafeed[self.security].get_new_bar()

            #self.current_bar = BarData(bar[0], bar[1], bar[2], bar[3], bar[4], bar[5])
          
            for i,j in enumerate(self.columns):
                setattr(self,j,bar[i])
            for i,j in enumerate(['datetime','open','high','low','close']):
                if j in self.columns:
                    pass
                else:
                    setattr(self,j,bar[i])

            self.current_bar = BarData(self.datetime, self.open, self.high, self.low, self.close, self.volume)  
            
            self.count += 1
            if not self.inited and self.count >= self.size:
                self.inited = True
  
            # [1,2,3,4,5,6,7,8,9,10]
            # [1,2,3,4,5,6,7,8,9] = [2,3,4,5,6,7,8,9,10]
            # [2,3,4,5,6,7,8,9,10, 10]
            self.open_array[:-1] = self.open_array[1:]
            self.high_array[:-1] = self.high_array[1:]
            self.low_array[:-1] = self.low_array[1:]
            self.close_array[:-1] = self.close_array[1:]
            self.volume_array[:-1] = self.volume_array[1:]
  
            # [2,3,4,5,6,7,8,9,10, 10] 然后最后一个数字被替换了.
            self.open_array[-1] = self.open
            self.high_array[-1] = self.high
            self.low_array[-1] = self.low
            self.close_array[-1] = self.close
            self.volume_array[-1] = self.volume
          
          
                
        except BaseException:#TypeError:
            raise BacktestFinished

    def run(self):
        self.update_bar()
    
    

