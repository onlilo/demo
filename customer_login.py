#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:46:41 2022

@author: arjun
"""

import jwt
import psycopg2
import hashlib, binascii
import pandas as pd
from datetime import datetime, timedelta
from .config import db_config,jwt_config



# import jwt
# encoded_jwt = jwt.encode({"some": "payload"}, JWT_SECRET, algorithm="HS256")
# print(encoded_jwt)
# jwt.decode(encoded_jwt, JWT_SECRET, algorithms=["HS256"])


class Login(object):
    def __init__(self,data):
        self.data = data
        self.JWT_SECRET = jwt_config["JWT_SECRET"]
        self.JWT_ALGORITHM = jwt_config["JWT_ALGORITHM"]
        self.JWT_EXP_DELTA_SECONDS = int(jwt_config["JWT_EXP_DELTA_SECONDS"])
        self.password_secret = jwt_config["PASSWORD_HASH"]        
        self.conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port']
                                )
        
    def user_authentication(self):
        try:
            username = self.data["username"].lower().strip()
            select_qry = """SELECT "password","Id" FROM public.users where user_name = %(user_name)s;"""
            select_qry_dict={"user_name":str(username)}
            user_data =  pd.read_sql(select_qry,self.conn,params =select_qry_dict)
            self.conn.close()
            if user_data.empty:
                return {"status":"Fail","status_code":401}
            else:
                user_id = user_data["Id"][0]
                password = self.data["password"]
                salt = hashlib.sha256(self.password_secret.encode('ascii')).hexdigest().encode('ascii')
                pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      password.encode('utf-8'),salt,100000)
                pwdhash = binascii.hexlify(pwdhash).decode('ascii')
                if (pwdhash == user_data["password"][0]):
                    payload = {
                    'user_id': int(user_id),
                    'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
                    }
                    jwt_token = jwt.encode(payload, self.JWT_SECRET, algorithm = self.JWT_ALGORITHM)
                    token = jwt_token.decode('utf-8')
                    return {"token":jwt_token,"status_code":200}
                else:
                    return {"status":"Fail","status_code":500}                    
        except Exception as e:
            print(str(e))
            self.conn.close()
            return {"status":"Fail","status_code":500}
        
# data = {"username":"pawzmo","password":"pawzmo123"}
# classs = Login(data)
# result = classs.user_authentication()