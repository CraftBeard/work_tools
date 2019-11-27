#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:01:16 2019

@author: Alex
"""

import os

# delete drive
os.system(r"net use Q: /del")

# map drive
os.system(r"net use Q: \\server_path\folder_name")