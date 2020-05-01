# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 20:23:05 2020

@author: xiubote
"""

import pymysql
import pandas as pd
import datetime
from XiuPy.share import XiuPyEnvBase, Environment, EventEngine

class Datafeed_sql(XiuPyEnvBase):
    
    def __init__(self, username, password, database, startdate, enddate, frequency, security):
        self._username = username
        self._password = password
        self.frequency = frequency
        self.security = security
        self.env.security.append(security)
        self.columns = []
        conn = pymysql.connect(user = self._username, password = self._password, database = database)
        self.cursor = conn.cursor()
        sql = "select d_day,open,high,low,close,volume from md_day where contract = '"+ self.security +"' and d_day >'"+str(startdate)+"' and d_day <'"+str(enddate)+"'"
        self.cursor.execute(sql)
        for i in self.cursor.description:
            self.columns.append(i[0])
        conn.close()
        
    def get_new_bar(self):
        return self.cursor.fetchone()
            
   
class Datafeed_csv(XiuPyEnvBase):
    
    def __init__(self, path, startdate, enddate, frequency, security):
        import datetime
        dataframe = pd.read_csv(path, index_col=0, parse_dates=True)
        self.security = security
        self.env.security.append(security)
        self.columns = ['datetime']+list(dataframe.columns)
        self.count = 0
        if frequency == 'day':
            if type(list(dataframe.index)[0]) == datetime.date or type(self.datetime[0]) == datetime.datetime:
                print(1)
            else:
                dataframe.index = [x.to_pydatetime().date() for x in list(dataframe.index)]
        else:
            if type(list(dataframe.index)[0]) == datetime.date or type(self.datetime[0]) == datetime.datetime:
                pass
            else:
                dataframe.index = [x.to_pydatetime() for x in list(dataframe.index)]
        dataframe = dataframe[(dataframe.index > startdate) & (dataframe.index < enddate)]
        self.datetime = list(dataframe.index)
        self.data = dataframe.values
        
    def get_new_bar(self):
        bar = [self.datetime[self.count]] + list(self.data[self.count])
        self.count +=1
        return bar

            
class Datafeed_dataframe(XiuPyEnvBase):
    
    def __init__(self, dataframe, startdate, enddate, frequency, security):
        import datetime
        self.security = security
        self.env.security.append(security)
        self.columns = ['datetime']+list(dataframe.columns)
        self.count = 0
        if frequency == 'day':
            if type(list(dataframe.index)[0]) == datetime.date or type(self.datetime[0]) == datetime.datetime:
                print(1)
            else:
                dataframe.index = [x.to_pydatetime().date() for x in list(dataframe.index)]
        else:
            if type(list(dataframe.index)[0]) == datetime.date or type(self.datetime[0]) == datetime.datetime:
                pass
            else:
                dataframe.index = [x.to_pydatetime() for x in list(dataframe.index)]
        dataframe = dataframe[(dataframe.index > startdate) & (dataframe.index < enddate)]
        self.datetime = list(dataframe.index)
        self.data = dataframe.values

        
    def get_new_bar(self):
        bar = [self.datetime[self.count]] + list(self.data[self.count])
        self.count +=1
        return bar


class Datafeed_wind(XiuPyEnvBase):
    """
    支持从wind接口下载数据
    具体api文档请访问万德
    """    
    def __init__(self, startdate, enddate, frequency, security):
        from WindPy import w
        w.start()
        self.security = security
        self.env.security.append(security)
        self.count = 0
        if frequency == 'day':
            self.data = w.wsd(security, "open,high,low,close,volume", str(startdate), str(enddate), "PriceAdj=B")
            self.columns = ['datetime']+[x.lower() for x in self.data.Fields]
        else:
            print('to be continued')
    def get_new_bar(self):
        bar = [self.data.Times[self.count]]
        for i in self.data.Data:
            bar.append(i[self.count])
        self.count += 1
        return bar
        
    
class Datafeed_baostock(XiuPyEnvBase):
    """
    支持从baostock接口下载数据
    具体api文档请访问baostock.com
    """
    def __init__(self, startdate, enddate, frequency, security):
        import baostock as bs
        bs.login()
        self.security = security
        self.env.security.append(security)
        self.frequency = frequency
        if frequency == 'day':
            self.rs = bs.query_history_k_data_plus(security,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                                  start_date=str(startdate), end_date=str(enddate),frequency="d", adjustflag="2")
            self.columns = self.rs.fields
        else:
            print('to be continued')
        
    def get_new_bar(self):
        if self.frequency == 'day':
            if self.rs.next():        
                bar = self.rs.get_row_data()
                bar[0] = datetime.datetime.strptime(bar[0], '%Y-%m-%d').date()
                return bar
            else:
                raise IndexError
        

    
    
    
    
    
    
    
