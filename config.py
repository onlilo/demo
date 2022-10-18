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
dotenv_path = Path('/home/ubuntu/.env')
load_dotenv(dotenv_path=dotenv_path)


db_config = {'user' : os.getenv('user'),
            'password' : os.getenv('password'),
            'host' : os.getenv('host'),
            'port' : os.getenv('port'),
            'database' : os.getenv('database')
            }


