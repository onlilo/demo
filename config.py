#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 12:26:47 2022

@author: arjun
"""

import os
# from pathlib import Path
from dotenv import load_dotenv

# # dotenv_path = Path('/home/arjun/.env')
# dotenv_path = Path('/home/ubuntu/demo/demo/.env')
# load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

db_config = {'user' : os.getenv('user'),
            'password' : os.getenv('password'),
            'host' : os.getenv('host'),
            'port' : os.getenv('port')
            }


jwt_config = {'JWT_SECRET' : os.getenv('JWT_SECRET'),
            'JWT_ALGORITHM' : os.getenv('JWT_ALGORITHM'),
            'JWT_EXP_DELTA_SECONDS' : os.getenv('JWT_EXP_DELTA_SECONDS'),
            'PASSWORD_HASH':os.getenv('PASSWORD_HASH')
            }
