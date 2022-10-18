#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 12:26:47 2022

@author: arjun
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# dotenv_path = Path('/home/arjun/.env')
dotenv_path = Path('/home/ubuntu/demo/demo.env')
load_dotenv(dotenv_path=dotenv_path)


db_config = {'user' : os.getenv('user'),
            'password' : os.getenv('password'),
            'host' : os.getenv('host'),
            'port' : os.getenv('port')
            }

# db_config = {'user' : "postgres",
#             'password' :"onlilo123",
#             'host' : "database-1.cmqsecpalehs.ap-south-1.rds.amazonaws.com",
#             'port' : "5432"
#             }