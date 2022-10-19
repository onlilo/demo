#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 12:59:19 2022

@author: arjun
"""

import jwt
import psycopg2
import hashlib, binascii
import pandas as pd
from datetime import datetime, timedelta
from .config import db_config,jwt_config

class Devices(object):
    def __init__(self,data):
        self.data = data
        self.JWT_SECRET = jwt_config["JWT_SECRET"]
        self.JWT_ALGORITHM = jwt_config["JWT_ALGORITHM"]
        self.JWT_EXP_DELTA_SECONDS = int(jwt_config["JWT_EXP_DELTA_SECONDS"])
        self.conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port']
                                )
    def device_details(self):
        token = self.data["token"]
        user_id = jwt.decode(token, options={"verify_signature": False})["user_id"]
        select_qry = """SELECT "id","name","is_default","battery","last_active" FROM public.devices where user_id = %(user_id)s;"""
        select_qry_dict={"user_id":int(user_id)}
        device_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
        self.conn.close()
        if device_data.empty:
            return {"status":"Fail","status_code":401,"Message":"No devices registered"}        
        else:
            return(device_data.to_dict('records'))

# data = {
#     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NjYxNzQwNDJ9.z5L2634hJWnk_6od9QLPayRbaStI-pP27Om2Z7li8Lo",
#     "status_code": 200
# }            
# classs = Devices(data)
# result = classs.device_details()
# print(result)


