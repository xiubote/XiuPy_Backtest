# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 22:45:07 2020

@author: xiubote
"""

from XiuPy.share import Environment, EventEngine, BarData, XiuPyEnvBase
from XiuPy.order import Order

class BaseStrategy(XiuPyEnvBase):

    broker = None  

    def __init__(self):
        self.type = 'Strategy'


    def on_start(self):
        """
        策略开始运行
        """

    def on_stop(self):
        """
        策略运行结束
        """

    def next_bar(self):
        raise NotImplementedError("请在子类中实现该方法")

    def run(self):
        self.next_bar()

    def buy(self, security, volume, limit_price = None):
        """
        期货做多/现货买
        :param price: 价格
        :param volume: 数量
        """
        print('buy create@'+str(self.env.datas[security].current_bar.datetime)+' '+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, volume, ordertype = 'buy', limit_price = None)
        self.env.order_pending.append(order)
       




    def sell(self, security, volume, limit_price = None):
        """
        期货合约平多/现货卖
        :param price: 价格
        :param volume: 数量
        """
        print('sell create@'+str(self.env.datas[security].current_bar.datetime)+' '+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, -volume, ordertype = 'sell', limit_price = None)
        self.env.order_pending.append(order)


    def short(self, security, volume, limit_price = None):
        """
        期货做空
        :param price: 价格
        :param volume: 数量
        """

        print('short create@'+str(self.env.datas[security].current_bar.datetime)+'  '+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, -volume, ordertype = 'short', limit_price = None)
        self.env.order_pending.append(order)
        
        
    def cover(self, security, volume, limit_price = None):
        """
        做空平仓
        :param price: 价格
        :param volume: 数量
        """

        print('cover create'+str(self.env.datas[security].current_bar.datetime)+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, volume, ordertype = 'cover', limit_price = None)
        self.env.order_pending.append(order)
        
    def close(self, security, limit_price = None):
        """
        做空平仓,
        :param price: 价格
        :param volume: 数量
        :return:
        """

        print('close create@'+str(self.env.datas[security].current_bar.datetime)+' '+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, volume = None, ordertype = 'close', limit_price = None)
        self.env.order_pending.append(order)
        
    def cancel(self, security, volume, limit_price = None):


        print('buy create'+str(self.env.datas[security].current_bar.datetime)+str(self.env.datas[security].current_bar.close))
        bar = self.env.datas[security].current_bar

        order = Order(bar.datetime, bar.close, security, volume, ordertype = 'cancel', limit_price = None)
        self.env.order_pending.append(order)

