#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:57:08 2022

@author: arjun
"""

import psycopg2
import pandas as pd
from datetime import datetime
from .config import db_config

class Dash(object):
    def __init__(self,data):
        self.data = data
        self.conn = psycopg2.connect(user = db_config['user'],
                            password = db_config['password'],
                            host = db_config['host'],
                            port = db_config['port']
                            )
    def GetData(self):
        try:
            date = self.data["date"]
            select_qry = """SELECT "Time","activity" FROM public.readings where "Date" = %(date)s;"""
            select_qry_dict={"date":date}
            dash_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
            dash_data = dash_data.drop_duplicates().sort_values(by=['Time'])
            self.conn.close()
            self.analytics_data = []
            
            for Activity  in ["Running","Barking"]:
                dash_data1 = dash_data.copy()
                dash_data1 = dash_data1.replace(Activity, 1)
                dash_data1 = dash_data1.fillna(0)
                dash_data1['consecutive'] = dash_data1.activity.groupby((dash_data1.activity != dash_data1.activity.shift()).cumsum()).transform('size') * dash_data1.activity
                dash_data1 = dash_data1[dash_data1.consecutive != 1]
                isB = dash_data1['activity'].eq(1)
                mask = isB & (~(isB.shift() & isB.shift(-1)) )
                time = sorted(list(dash_data1["Time"][mask]))
            
                duration = []
                data_dict = {}
                data_dict["Activity"] = Activity
                for Time in range(len(time)-1):
                    start_time = time[Time]
                    end_time = time[Time+1]
                    t1 = datetime.strptime(start_time, "%H:%M:%S")
                    t2 = datetime.strptime(end_time, "%H:%M:%S")
                    delta = t2 - t1
                    if Time == 0:
                        duration.append(int(delta.total_seconds()))
                        duration.append(int(delta.total_seconds()))
                    else:
                        duration.append(int(delta.total_seconds())) 
                data_dict["time"] = time
                data_dict["duration"] = duration
                self.analytics_data.append(data_dict)
            return self.analytics_data
        except Exception as e:
            self.conn.close()
            return {"status":"Fail","error":str(e)}
            

        