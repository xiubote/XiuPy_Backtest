# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 22:45:07 2020

@author: xiubote
"""

import itertools
import numpy as np
import pandas as pd
import collections
from XiuPy.strategy import BaseStrategy
from XiuPy.share import XiuPyEnvBase, Environment, EventEngine, BarData
from XiuPy.market import Market, BacktestFinished
from XiuPy.order import Fill,Order,Analyzer


class Cerebro(XiuPyEnvBase):
    
    def __init__(self):
        self.datas = self.env.datas
        self.strategy_instance = None
        self.env.leverage = 1.0
        self.slipper_rate = 5/10000
        # 购买的资产的估值，作为计算爆仓的时候使用.
        self.asset_value = 0
        self.env.margin = 0.15
        self.env.cash = 10000
        self.strategy_class = None
        # 交易的数据.
        self.trades = []
        # 当前提交的订单.
        self.active_orders = []
        self.position = 0
        self.is_optimizing_strategy = False


    def set_strategy(self, strategy:BaseStrategy):
        self.strategy_class = strategy
        #self.env.strategy = strategy
        
    def set_margin(self, margin, security = None):
        self.env.margin = margin

    def set_leverage(self, leverage):
        self.env.leverage = leverage

    def set_commission(self, commission = 0):
        self.env.commission = commission

    def set_cash(self, cash = 10000):
        self.env.cash = cash
        
    def adddata(self, data):
        self.env.datafeed[data.security] = data




    def initialize_trading_system(self):

        for i in self.env.security:
              self.env.datas[i] = Market(i, size = 500)
              self.env.security_position[i] = 0
              self.env.fills[i] = Fill(i)
        self.ana = Analyzer()      
        self.strategy = self.strategy_class()
        self.strategy.broker = self
        self.strategy.on_start()
        self.pre_event = None
                
                
    def order_checker(self):
        
        for i,order in enumerate(self.env.order_pending[:]):
            if order.ordertype != 'close':
                if self.env.cash > order.volume * self.env.datas[order.security].current_bar.open * self.env.margin:
                    self.env.event_engine.put(order)
                    self.env.order_pending.remove(order)
            else:
                self.env.event_engine.put(order)
                self.env.order_pending.remove(order)
        self.pre_event = 'Order'
            
            
    def run(self):        
        self.initialize_trading_system()
        while True:
            try:
                
                if self.env.event_engine.is_empty():
                    if self.pre_event == None or self.pre_event == 'Analyzer':
                        for i in self.env.security:
                            self.env.event_engine.put(self.env.datas[i])
                        
                    elif self.pre_event == 'Market':
                        self.order_checker()
                        
                    elif self.pre_event == 'Order':
                        self.env.event_engine.put(self.strategy)
                        
                    elif self.pre_event == 'Strategy':
                        for i in self.env.security:
                            self.env.event_engine.put(self.env.fills[i])
                        
                    elif self.pre_event == 'Fill':
                        self.env.event_engine.put(self.ana)

                else:
                    self.cur_event = self.env.event_engine.get()
                    self.cur_event.run()
                    self.pre_event = self.cur_event.type
                    
            except BacktestFinished:
                self.strategy.on_stop()
                self.ana.on_stop()
                break

    def pending_order_checker(self):
        for i,order in enumerate(self.env.order_pending):
            if self.env.cash > order.volume * self.env.datas[order.security].current_bar.open * self.env.margin:
                order.run()
                self.env.order_pending.pop(i)

    def runny(self):        
        self.initialize_trading_system()
        while True:
            try:
                for i in self.env.security:
                    self.env.datas[i].update_bar()
                self.pending_order_checker()
                self.strategy.next_bar()
                for i in self.env.security:
                     self.env.fills[i].run()
                self.ana.run()
                    
            except BacktestFinished:
                self.strategy.on_stop()
                break



    def optimize_strategy(self, **kwargs):
        """
        优化策略， 参数遍历
        :param kwargs:
        :return:
        """
        self.is_optimizing_strategy = True

        optkeys = list(kwargs)
        vals = iterize(kwargs.values())
        optvals = itertools.product(*vals)  #
        optkwargs = map(zip, itertools.repeat(optkeys), optvals)
        optkwargs = map(dict, optkwargs)  # dict value...

        for params in optkwargs:
            print(params)

        # 参数列表, 要优化的参数, 放在这里.

        cash = self.cash
        leverage = self.leverage
        commission = self.commission
        for params in optkwargs:

            self.strategy_class.params = params
            self.set_cash(cash)
            self.set_leverage(leverage)
            self.set_commission(commission)
            self.run()

def iterize(iterable):
    '''Handy function which turns things into things that can be iterated upon
    including iterables
    '''
    niterable = list()
    for elem in iterable:
        if isinstance(elem, str):
            elem = (elem,)
        elif not isinstance(elem, collections.Iterable):
            elem = (elem,)

        niterable.append(elem)

    return niterable