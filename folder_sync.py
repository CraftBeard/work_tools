#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:09:28 2019

@author: Alex
"""

import os
import shutil

# directory paths
path_1 = r""
path_2 = r""

# confirmation
confirmation = input("Do you want to synchronize " + path_1 + " & " + path_2 + ": (Y/N)")

if confirmation != "Y":
	quit()

# compare modified datetimes of folders
modified_time_1 = os.path.getmtime(path_1)
modified_time_2 = os.path.getmtime(path_2)

src_path = ""
dest_path = ""

if modified_time_1 < modified_time_2:
	src_path, dest_path = path_1,path_2
elif modified_time_2 < modified_time_1:
	src_path, dest_path = path_2,path_1

# overwrite old folder with new one
if src_path != "":
	shutil.copytree(src_path, dest_path)