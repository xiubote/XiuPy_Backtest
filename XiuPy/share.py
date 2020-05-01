# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:05 2020

@author: xiubote
"""

import queue
from collections import defaultdict,OrderedDict


class EventEngine(object):
    def __init__(self):
        self._core = queue.Queue()  
        
    def put(self, event):
        self._core.put(event)

    def get(self):
        return self._core.get(block = False)

    def is_empty(self) -> bool:
        return self._core.empty()
    
class BarData(object):
    """
    K 线数据模型
    """
    def __init__(self, datetime, open_price, high_price, low_price, close_price, volume):
        self.datetime = datetime
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume

    def __str__(self):
        return f"{self.datetime} {self.open_price} {self.high_price} {self.low_price} {self.close_price}"


class Environment(object):
    """作为全局共享变量为各模块提供支持"""

    event_engine = EventEngine()
    security = []
    order = []
    order_pending = []
    order_image = {}
    trade_image = []
    current_datetime = 0
    datas = {}
    datafeed = {}
    fills = {}
    margin_rate = 0.15
    cash = 100000
    asset = cash
    leverage = 1.0
    slipper_rate = 0
    
    strategy_class = None
    position = 0
    security_position = {}


    # general context
    sys_date: str = None
    sys_frequency: str = None
    instrument: str = None
    fromdate: str = None
    todate: str = None
    tickers: list = []


    # system memory
    signals_normal: list = []  # 保存最原始的所有信号
    signals_pending: list = []  # 保存最原始的所有挂单信号
    signals_trigger: list = []  # 保存最原始的所有触发单信号
    signals_cancel: list = []  # 保存最原始的所有挂单信号

    # 动态地临时信号, 会不断刷新
    signals_normal_cur: list = []
    signals_pending_cur: list = []
    signals_trigger_cur: list = []
    signals_cancel_cur: list = []


    orders_pending: list = []   # 动态地保存挂单,触发会删除

    orders_cancel_cur: list = []  # 动态地保存撤单, 会不断刷新
    orders_cancel_submitted_cur: list = []  # 动态地保存撤单, 会不断刷新

    cur_suspended_tickers: list = []  # 动态保存当前停牌或者没更新数据的ticker
    #suspended_tickers_record: defaultdict = defaultdict(list)  # 记录停牌


    @classmethod
    def initialize_env(cls):
        """刷新environment防止缓存累积"""
        cls.signals_normal.clear()



class XiuPyEnvBase(object):
    """作为基类，提供env共享给各个模块"""
    env = Environment