# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 18:13:16 2020

@author: xiubote
"""

from XiuPy.share import Environment, EventEngine, BarData, XiuPyEnvBase
import datetime
from collections import OrderedDict

#class Trade_generator(XiuPyEnvBase):
#    def __init__(self, order):
#        self.security = order.security
#        self.volume = order.volume
#        self.price_in = self.env.datas[order.security].current_bar.open
#        self.temp = self.price_in
#        self.date_in = self.env.datas[order.security].current_bar.datetime
#        self.env.security_position[self.security] += order.volume
#        print(self.price_in)
#        print(self.date_in)
        
        
class Order(XiuPyEnvBase):
    def __init__(self, datetime, price, security, volume, ordertype, limit_price = None):
        self.create_date = datetime
        self.create_price = price
        self.security = security
        self.volume = volume
        self.ordertype = ordertype
        self.type = 'Order'
    

    def run(self):
#        if self.env.cash > self.volume * self.env.datas[self.security].current_bar.open * self.env.margin:
            self.env.fills[self.security].order_execute(self)
     
        
        
class Fill(XiuPyEnvBase):
    def __init__(self, security):
        self.type = 'Fill'
        self.security = security
        
    
    def order_execute(self,order):
#        if self.env.cash > order.volume * self.env.datas[self.security].current_bar.open * self.env.margin:
            if order.ordertype == 'buy' or order.ordertype == 'sell':
                p = self.env.security_position[self.security]
                if p == 0:
                    
                    self.margin = order.volume * self.env.datas[self.security].current_bar.open * self.env.margin
                    self.env.cash -= self.margin
                    self.env.security_position[self.security] = order.volume
                    self.last = order.volume * self.env.datas[self.security].current_bar.open
                    self.trade_float = 0
                    
                elif p*(p+order.volume) > 0:
                    
                    self.float_profit = p * self.env.datas[self.security].current_bar.open - self.last
                    self.env.asset += self.float_profit
                    
                    self.env.security_position[self.security] = p+order.volume
                    self.last = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.open
                    
                    self.margin_change = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.open * self.env.margin - self.margin
                    self.margin = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.open * self.env.margin
                    self.env.cash += (self.float_profit - self.margin_change)
                    #self.env.cash = self.env.asset-self.margin
                    
                    self.trade_float += self.float_profit
                                
             
                elif p*(p+order.volume) <= 0:

                    self.float_profit = p * self.env.datas[self.security].current_bar.open - self.last
                    self.env.asset += self.float_profit
                    self.trade_float += self.float_profit
                    self.env.trade_image.append(self.trade_float)
                    
                    self.env.security_position[self.security] = 0
                    self.env.cash += self.margin +self.float_profit
                    
                    self.margin = (p+order.volume) * self.env.datas[self.security].current_bar.open * self.env.margin
                    self.env.cash -= self.margin
                    self.env.security_position[self.security] = (p+order.volume)
                    
                    self.last = (p+order.volume) * self.env.datas[self.security].current_bar.open
                    self.trade_float = 0
                    
            elif order.ordertype == 'close':
                p = self.env.security_position[self.security]
                self.float_profit = p * self.env.datas[self.security].current_bar.open - self.last
                self.env.asset += self.float_profit
                self.env.cash += self.margin + self.float_profit
                self.trade_float += self.float_profit
                self.env.trade_image.append(self.trade_float)
                    
                self.env.security_position[self.security] = 0
                
                
            
              
    def pending_order_checker(self):
        for order in self.env.order_pending:
            self.order_execute()
            
    def run(self):
        if self.env.security_position[self.security] != 0:
            self.float_profit = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.close - self.last
            self.last = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.close
            self.margin_change = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.close * self.env.margin - self.margin
            self.margin = self.env.security_position[self.security] * self.env.datas[self.security].current_bar.close * self.env.margin
            self.env.cash += self.float_profit - self.margin_change
            self.env.asset += self.float_profit
            self.trade_float += self.float_profit

              

              
              
class Analyzer(XiuPyEnvBase):
    def __init__(self):
        self.type = 'Analyzer'
        self.datatime_list = []
        self.cash_list = []
        self.asset_list = []
        self.position_list = []
        self.cash_dict = OrderedDict()
        self.asset_dict = OrderedDict()
        self.position_dict = OrderedDict()
        self.margin_dict = OrderedDict()
        

    def run(self):
        self.datatime_list.append(self.env.datas[self.env.security[0]].current_bar.datetime)
        self.cash_list.append(self.env.cash)
        self.asset_list.append(self.env.asset)
        self.position_list.append((self.env.asset-self.env.cash)/self.env.asset)
        if type(self.env.datas[self.env.security[0]].current_bar.datetime) == datetime.date:
            self.cash_dict[self.env.datas[self.env.security[0]].current_bar.datetime] = self.env.cash
            self.asset_dict[self.env.datas[self.env.security[0]].current_bar.datetime] = self.env.asset
            self.position_dict[self.env.datas[self.env.security[0]].current_bar.datetime] = (self.env.asset-self.env.cash)/self.env.asset
        elif type(self.env.datas[self.env.security[0]].current_bar.datetime) == datetime.datetime:
            self.cash_dict[self.env.datas[self.env.security[0]].current_bar.datetime.date()] = self.env.cash
            self.asset_dict[self.env.datas[self.env.security[0]].current_bar.datetime.date()] = self.env.asset
            self.position_dict[self.env.datas[self.env.security[0]].current_bar.datetime.date()] = (self.env.asset-self.env.cash)/self.env.asset
        
      
      
    def on_stop(self):
        pass





