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
            date = self.data["date"]
            select_qry = """SELECT * FROM public.readings where "device_id" = %(device_id)s AND "Date" = %(date)s;"""
            select_qry_dict={"device_id":int(device_id),"date":date}
            source_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
            source_data = source_data.fillna("")
            source_data = source_data.drop(["id"], axis=1)
            source_data = source_data.to_dict('records')
            self.conn.close()          
            return source_data
        except:
            self.conn.close()
            return {"Status":"Fail","status_code":500}
        
    def update_data(self):
        try:
            device_id = self.data["device_id"]
            date = self.data["Date"]
            time = self.data["Time"]
            activity = self.data["activity"]
            update_query = """UPDATE public.readings SET "activity" = %(activity)s WHERE "Date"= %(date)s AND "Time"= %(time)s AND "device_id"= %(device_id)s;"""
            update_qry_dict={"device_id":int(device_id),"date":date,"time":time,"activity":activity}
            self.cur.execute(update_query,update_qry_dict)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return {"Status":"Success","status_code":200}
        except:
            self.cur.close()
            self.conn.close()
            return {"Status":"Fail","status_code":500}
        

