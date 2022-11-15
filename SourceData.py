#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:20:11 2022

@author: arjun
"""

import psycopg2
import pandas as pd
from .config import db_config

class ViewData(object):
    def __init__(self,data):
        self.data = data       
        self.conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port']
                                )    
        self.cur = self.conn.cursor()
        
    def view_data(self):
        try:
            device_id = self.data["id"]
            date = self.data["Date"]
            select_qry = """SELECT * FROM public.readings where "device_id" = %(device_id)s AND "Date" = %(date)s;"""
            select_qry_dict={"device_id":int(device_id),"date":date}
            source_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
            source_data = source_data.fillna("")
            source_data = source_data.drop(["id"], axis=1)
            source_data = source_data.sort_values(by=['Time'])
            source_data = source_data.to_dict('records')
            self.conn.close()          
            return source_data
        except Exception as e:
            self.conn.close()
            return {"status":"Fail","error":str(e)}
        
    def update_data(self):
        try:
            device_id = self.data[0]["device_id"]
            date = tuple([ data["Date"] for data in self.data])
            time = tuple([ data["Time"] for data in self.data])
            activity = self.data[0]["activity"]
            if activity == "No activity":
                activity = None
            update_query = """UPDATE public.readings SET "activity" = %(activity)s WHERE "Date" in  %(date)s AND "Time" in %(time)s AND "device_id"= %(device_id)s;"""
            update_qry_dict={"device_id":int(device_id),"date":date,"time":time,"activity":activity}
            self.cur.execute(update_query,update_qry_dict)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return {"Status":"Success"}
        except Exception as e:
            self.cur.close()
            self.conn.close()
            return {"status":"Fail","error":str(e)}



