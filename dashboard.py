#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:57:08 2022

@author: arjun
"""

import psycopg2
import pandas as pd
from .config import db_config

class Dash(object):
    def __init__(self,data):
        self.data = data
        self.conn = psycopg2.connect(user = db_config['user'],
                            password = db_config['password'],
                            host = db_config['host'],
                            port = db_config['port']
                            )
        self.from_to = [("00:00:00","00:59:59"),("01:00:00","01:59:59"),("02:00:00","02:59:59"),("03:00:00","03:59:59"),
                   ("04:00:00","04:59:59"),("05:00:00","05:59:59"),("06:00:00","06:59:59"),
                   ("07:00:00","07:59:59"),("08:00:00","08:59:59"),("09:00:00","09:59:59"),
                   ("10:00:00","10:59:59"),("11:00:00","11:59:59"),("12:00:00","12:59:59"),("13:00:00","13:59:59"),
                   ("14:00:00","14:59:59"),("15:00:00","15:59:59"),("16:00:00","16:59:59"),("17:00:00","18:59:59"),
                   ("19:00:00","19:59:59"),("20:00:00","20:59:59"),("21:00:00","21:59:59"),("22:00:00","22:59:59"),
                   ("23:00:00","23:59:59"),("24:00:00","24:59:59")]
        self.MainList = []
    def GetData(self):
        try:
            from_date = self.data["from"]
            to_date = self.data["to"]
            if from_date == to_date:
                select_qry = """SELECT "Time","activity" FROM public.readings where "Date" = %(date)s;"""
                select_qry_dict={"date":from_date}
                dash_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
                dash_data = dash_data.drop_duplicates().sort_values(by=['Time'])
                activity_list = list(dash_data.activity.unique())
                if None in activity_list:
                    activity_list.remove(None)
                self.myDict = {key: {"time":[],"duration":[],"total_duration":None} for key in activity_list}
                
                for time_range in range(len(self.from_to)):
                    dash_data_copy = dash_data.copy()
                    dash_data_copy = dash_data_copy[dash_data_copy['Time'].between(self.from_to[time_range][0], self.from_to[time_range][1])]
                    if len(activity_list)>0:
                        for Activity in activity_list:
                            activities = dash_data_copy['activity'].tolist()
                            Activity_count = round(activities.count(Activity)/60)
                            if int(self.from_to[time_range][0].split(":")[0])==0:
                                self.myDict[Activity]["time"].append("12AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==1:
                                self.myDict[Activity]["time"].append("1AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==2:
                                self.myDict[Activity]["time"].append("2AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==3:
                                self.myDict[Activity]["time"].append("3AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==4:
                                self.myDict[Activity]["time"].append("4AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==5:
                                self.myDict[Activity]["time"].append("5AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==6:
                                self.myDict[Activity]["time"].append("6AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==7:
                                self.myDict[Activity]["time"].append("7AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==8:
                                self.myDict[Activity]["time"].append("8AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==9:
                                self.myDict[Activity]["time"].append("9AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==10:
                                self.myDict[Activity]["time"].append("10AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==11:
                                self.myDict[Activity]["time"].append("11AM")
                            elif int(self.from_to[time_range][0].split(":")[0])==12:
                                self.myDict[Activity]["time"].append("12PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==13:
                                self.myDict[Activity]["time"].append("1PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==14:
                                self.myDict[Activity]["time"].append("2PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==15:
                                self.myDict[Activity]["time"].append("3PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==16:
                                self.myDict[Activity]["time"].append("4PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==17:
                                self.myDict[Activity]["time"].append("5PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==18:
                                self.myDict[Activity]["time"].append("6PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==19:
                                self.myDict[Activity]["time"].append("7PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==20:
                                self.myDict[Activity]["time"].append("8PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==21:
                                self.myDict[Activity]["time"].append("9PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==22:
                                self.myDict[Activity]["time"].append("10PM")
                            elif int(self.from_to[time_range][0].split(":")[0])==23:
                                self.myDict[Activity]["time"].append("11PM") 
                            else:
                                pass
                            if Activity_count>0:
                                self.myDict[Activity]["duration"].append(str(Activity_count))
                            else:
                                self.myDict[Activity]["duration"].append("")
                for entries in self.myDict:
                    SubDict = {}
                    SubDict["activity"] =entries 
                    SubDict["time"] = self.myDict[entries]["time"]
                    SubDict["duration"] = self.myDict[entries]["duration"]
                    filtered_duration = filter(lambda x: len(x)>0, self.myDict[entries]["duration"])
                    total_duaration = map(int,list(filtered_duration))
                    SubDict["total_duration"] = sum(total_duaration)
                    self.MainList.append(SubDict)
            else:
                pass
            self.conn.close()
            return self.MainList
        
        except Exception as e:
            self.conn.close()
            return {"status":"Fail","error":str(e)}
            

# data = {"from":"2022-11-07","to":"2022-11-07"}       
# cls = Dash(data)
# result = cls.GetData()
# print(result)