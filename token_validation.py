#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:03:51 2021

@author: arjun
"""

import jwt
from .config import jwt_config
from django.http import JsonResponse


def token_authentication(function):
    def wrapper_accepting_arguments(request):
        try:
            auth = request.headers['Authorization']
            token = auth.split()[1]
            JWT_SECRET = jwt_config["JWT_SECRET"]
            JWT_ALGORITHM = jwt_config["JWT_ALGORITHM"]
            jwt.decode(token,JWT_SECRET,JWT_ALGORITHM)
        except:
            return JsonResponse({"status":"Unauthorized Access"},status = 401)
        return function(request)
    return wrapper_accepting_arguments

