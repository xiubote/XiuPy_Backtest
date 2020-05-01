# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 22:45:07 2020

@author: xiubote
"""

import XiuPy as xp
import numpy as np
import pandas as pd
import datetime


class DemoStrategy(xp.BaseStrategy):

    params = {'long_period': 110, 'short_period': 70}

    def __init__(self):
        super().__init__()

    def on_start(self):
        print("策略开始运行")

    def on_stop(self):
        print("策略停止运行")
    
    def notify_order(self):
        pass
        
    def notify_trade(self):
        pass

    def next_bar(self):

        print(self.env.datas['if00'].current_bar)
#        print(self.env.datas['if00'].current_bar.datetime)
#        print(self.env.security_position['if00'])
#        print(self.env.security_position['ih00'])

#        if self.env.datas['if00'].current_bar.datetime == datetime.date(2019, 6, 3):
#            self.sell('if00', 2)
#
#            
#        if self.env.datas['if00'].current_bar.datetime == datetime.date(2019, 6, 13):
#            self.buy('if00',3)
#        
#        if self.env.datas['if00'].current_bar.datetime == datetime.date(2019, 6, 3):
#            self.sell('ih00', 2)
#            
#        if self.env.datas['if00'].current_bar.datetime == datetime.date(2019, 6, 13):
#            self.buy('ih00',2)
#            
#        if self.env.datas['if00'].current_bar.datetime == datetime.date(2019, 6, 25):
#            self.close('if00')


if __name__ == '__main__':

    data = xp.Datafeed_sql(username = 'root', password = '58604496', database = 'future',
            startdate = datetime.date(2019, 1, 2),
            enddate = datetime.date(2019, 6, 30),
            frequency = 'day', security = 'if00')
    
    data2 = xp.Datafeed_sql(username = 'root', password = '58604496', database = 'future',
            startdate = datetime.date(2019, 1, 2),
            enddate = datetime.date(2019, 6, 30),
            frequency = 'day', security = 'ih00')
    

    
    #data3 =  xp.datafeed_csv(path = 'bitmex_btc_usd_1min_data.csv',
    #        startdate=datetime.date(2019, 1, 1),
    #        enddate=datetime.date(2019, 1, 2),
    #        frequency = 'min',
    #        security = ['bit'])


    cerebro = xp.Cerebro()    
    cerebro.adddata(data)
    cerebro.adddata(data2)
    cerebro.set_strategy(DemoStrategy)
    cerebro.set_margin(0.15)
    cerebro.set_cash(100000)  # 100万初始资金.
    cerebro.run()

    # 参数优化， 穷举法， 遗传算法。
    # broker.optimize_strategy(long_period=[i for i in range(100, 300, 10)], short_period=[i for i in range(50, 100, 5)])


#a=cerebro.ana
#b=a.cash_dict
#c=a.asset_dict

